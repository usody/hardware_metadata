.PHONY: build
build:
	build/build_workbench.sh

# faster build for debugging/development purposes
#   on pedro's laptop the difference is around 14s vs 1min20s
build_dev:
	DEBUG=1 build/build_workbench.sh

# force build of bullseye
build_bullseye:
	VERSION_CODENAME='buster' build/build_workbench.sh

cleanBuild:
	# TODO hardcoded
	rm -rf staging/live/filesystem.squashfs

run:
	python3 workbench_lite.py

test:
	python3 test.py

bootiso:
	qemu-system-x86_64 -enable-kvm -m 2G -vga qxl -netdev user,id=wan -device virtio-net,netdev=wan,id=nic1 -drive file=build/wbiso/debian-wb-lite.iso,cache=none,if=virtio;

