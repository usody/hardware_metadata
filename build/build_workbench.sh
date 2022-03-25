#!/bin/sh -e

set -x

# TODO encapsulate into functions

# TODO verify sudo situation

hostname='workbench-live'

# detect non root user without sudo
if [ "$(id -u)" -ne 0 ] && id $USER | grep -qv sudo; then
  echo "ERROR: this script needs root or sudo permissions (current user is not part of sudo group)"
  exit 1
# detect user with sudo or already on sudo src https://serverfault.com/questions/568627/can-a-program-tell-it-is-being-run-under-sudo/568628#568628
elif [ "$(id -u)" -ne 0 ] || [ -n "${SUDO_USER}" ]; then
  SUDO='sudo'
  # jump to current dir where the script is so relative links work
  cd "$(dirname "${0}")"
  # workbench working directory to build the iso
  WB_PATH="wbiso"
# detect pure root
elif [ "$(id -u)" -e 0 ]; then
  SUDO=''
  WB_PATH="/opt/workbench_live_dev"
fi

# version of debian the bootstrap is going to build
#   if no VERSION_CODENAME is specified we assume that the bootstrap is going to
#   be build with the same version of debian being executed because some files
#   are copied from our root system
if [ -z "${VERSION_CODENAME}" ]; then
  . /etc/os-release
  echo "TAKING OS-RELEASE FILE"
fi

mkdir -p ${WB_PATH}

# Install requirements
${SUDO} apt-get update
${SUDO} apt-get install -y \
  debootstrap \
  squashfs-tools \
  xorriso \
  grub-pc-bin \
  grub-efi-amd64-bin \
  mtools


chroot_path="${WB_PATH}/chroot"
if [ ! -d "${chroot_path}" ]; then
  ${SUDO} debootstrap --arch=amd64 --variant=minbase ${VERSION_CODENAME} ${WB_PATH}/chroot http://deb.debian.org/debian/
  # TODO does this make sense?
  ${SUDO} chown -R "${USER}:" ${WB_PATH}/chroot
fi

wb_dir="${WB_PATH}/chroot/opt/workbench"
mkdir -p "${wb_dir}"
cp ../workbench_lite.py "${wb_dir}"
# private repo
#git clone https://github.com/usody/workbench-lite.git "${wb_temp}"
# Select workbench branch to build
# git checkout testing
#cd -

# non interactive chroot -> src https://stackoverflow.com/questions/51305706/shell-script-that-does-chroot-and-execute-commands-in-chroot
${SUDO} chroot ${WB_PATH}/chroot <<END

echo "${hostname}" > /etc/hostname

# check what linux images are available on the system
# Figure out which Linux Kernel you want in the live environment.
#   apt-cache search linux-image

backports_repo='deb http://deb.debian.org/debian ${VERSION_CODENAME}-backports main contrib'
printf "\${backports_repo}" > /etc/apt/sources.list.d/backports.list

# Installing packages
apt-get update && \
apt-get install -y --no-install-recommends \
  linux-image-amd64 \
  live-boot \
  systemd-sysv

### START workbench_lite installation

echo 'Install Workbench'

#Disable systemd-logind acpi handling
echo '[Login]' >/etc/systemd/logind.conf
echo "HandlePowerKey=ignore" >>/etc/systemd/logind.conf
systemctl enable acpid

#Override acpid power handling
echo "/bin/systemctl poweroff --force --force --force" >/etc/acpi/powerbtn-acpi-support.sh
### END workbench-live installation

# other utilities
apt-get install -t ${VERSION_CODENAME}-backports lshw

# first line is workbench requirements.debian.txt
apt-get install --no-install-recommends \
  python3 python3-dev dmidecode smartmontools hwinfo \
  sudo \
  curl openssh-client \
  less \
  jq \
  nano vim-tiny && \
apt-get clean

# Set up root user & exit

# this is the root password
# Method3: Use echo
#   src https://www.systutorials.com/changing-linux-users-password-in-one-command-line/
#   TODO hardcoded password
echo -e 'workbench\nworkbench' | passwd
END


# Creating directories
mkdir -p ${WB_PATH}/staging/EFI/boot
mkdir -p ${WB_PATH}/staging/boot/grub/x86_64-efi
mkdir -p ${WB_PATH}/staging/isolinux
mkdir -p ${WB_PATH}/staging/live
mkdir -p ${WB_PATH}/tmp

# Compress chroot folder

# Faster squashfs when debugging -> src https://forums.fedoraforum.org/showthread.php?284366-squashfs-wo-compression-speed-up
if [ "${DEBUG}" ]; then
  DEBUG_SQUASHFS_ARGS='-noI -noD -noF -noX'
fi

# why squashfs -> https://unix.stackexchange.com/questions/163190/why-do-liveusbs-use-squashfs-and-similar-file-systems
# noappend option needed to avoid this situation -> https://unix.stackexchange.com/questions/80447/merging-preexisting-source-folders-in-mksquashfs
${SUDO} mksquashfs \
  ${WB_PATH}/chroot \
  ${WB_PATH}/staging/live/filesystem.squashfs \
  ${DEBUG_SQUASHFS_ARGS} \
  -noappend -e boot \

# Copy kernel and initramfs
cp ${WB_PATH}/chroot/boot/vmlinuz-* \
  ${WB_PATH}/staging/live/vmlinuz && \
cp ${WB_PATH}/chroot/boot/initrd.img-* \
  ${WB_PATH}/staging/live/initrd

# boot grub
#   TIMEOUT 60 means 6 seconds :)
cat <<EOF >${WB_PATH}/staging/isolinux/isolinux.cfg
UI vesamenu.c32

MENU TITLE Boot Menu
DEFAULT linux
TIMEOUT 60
MENU RESOLUTION 640 480
MENU COLOR border       30;44   #40ffffff #a0000000 std
MENU COLOR title        1;36;44 #9033ccff #a0000000 std
MENU COLOR sel          7;37;40 #e0ffffff #20ffffff all
MENU COLOR unsel        37;44   #50ffffff #a0000000 std
MENU COLOR help         37;40   #c0ffffff #a0000000 std
MENU COLOR timeout_msg  37;40   #80ffffff #00000000 std
MENU COLOR timeout      1;37;40 #c0ffffff #00000000 std
MENU COLOR msg07        37;40   #90ffffff #a0000000 std
MENU COLOR tabmsg       31;40   #30ffffff #00000000 std

LABEL linux
  MENU LABEL Debian Live [BIOS/ISOLINUX]
  MENU DEFAULT
  KERNEL /live/vmlinuz
  APPEND initrd=/live/initrd boot=live

LABEL linux
  MENU LABEL Debian Live [BIOS/ISOLINUX] (nomodeset)
  MENU DEFAULT
  KERNEL /live/vmlinuz
  APPEND initrd=/live/initrd boot=live nomodeset
EOF

cat <<EOF >${WB_PATH}/staging/boot/grub/grub.cfg
search --set=root --file /DEBIAN_CUSTOM

set default="0"
set timeout=1

# If X has issues finding screens, experiment with/without nomodeset.

menuentry "Debian Live [EFI/GRUB]" {
    linux ($root)/live/vmlinuz boot=live
    initrd ($root)/live/initrd
}

menuentry "Debian Live [EFI/GRUB] (nomodeset)" {
    linux ($root)/live/vmlinuz boot=live nomodeset
    initrd ($root)/live/initrd
}
EOF

cat <<EOF >${WB_PATH}/tmp/grub-standalone.cfg
search --set=root --file /DEBIAN_CUSTOM
set prefix=($root)/boot/grub/
configfile /boot/grub/grub.cfg
EOF

touch ${WB_PATH}/staging/DEBIAN_CUSTOM

## Bootloaders

cp /usr/lib/ISOLINUX/isolinux.bin "${WB_PATH}/staging/isolinux/" && \
cp /usr/lib/syslinux/modules/bios/* "${WB_PATH}/staging/isolinux/"

cp -r /usr/lib/grub/x86_64-efi/* "${WB_PATH}/staging/boot/grub/x86_64-efi/"

grub-mkstandalone \
  --format=x86_64-efi \
  --output=${WB_PATH}/tmp/bootx64.efi \
  --locales="" \
  --fonts="" \
  "boot/grub/grub.cfg=${WB_PATH}/tmp/grub-standalone.cfg"

(
  cd ${WB_PATH}/staging/EFI/boot && \
    dd if=/dev/zero of=efiboot.img bs=1M count=20 && \
    mkfs.vfat efiboot.img && \
    mmd -i efiboot.img efi efi/boot && \
    mcopy -vi efiboot.img ../../../tmp/bootx64.efi ::efi/boot/
)

# Creating ISO

wbiso_file="${WB_PATH}/debian-wb-lite.iso"

xorriso \
  -as mkisofs \
  -iso-level 3 \
  -o "${wbiso_file}" \
  -full-iso9660-filenames \
  -volid "DEBIAN_CUSTOM" \
  -isohybrid-mbr /usr/lib/ISOLINUX/isohdpfx.bin \
  -eltorito-boot \
    isolinux/isolinux.bin \
    -no-emul-boot \
    -boot-load-size 4 \
    -boot-info-table \
    --eltorito-catalog isolinux/isolinux.cat \
  -eltorito-alt-boot \
    -e /EFI/boot/efiboot.img \
    -no-emul-boot \
    -isohybrid-gpt-basdat \
  -append_partition 2 0xef ${WB_PATH}/staging/EFI/boot/efiboot.img \
  "${WB_PATH}/staging"

printf "\n\n  image generated in build/${wbiso_file}\n\n"

# Execute iso
# qemu-system-x86_64 -enable-kvm -m 2G -vga qxl -netdev user,id=wan -device virtio-net,netdev=wan,id=nic1 -drive file=debian-wb-lite.iso,cache=none,if=virtio;
