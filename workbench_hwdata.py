import subprocess
import json

class HardwareData:
    """ Collect as much hardware data as possible using lshw, dmidecode, lspci and others tools."""

    def get_lshw_data():
        """Get hw data using lshw command and return dict."""
        lshw_command = ['lshw -json']
        proc = subprocess.Popen(lshw_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lshw_output, lshw_errors = proc.communicate()
        proc.wait()

        lshw_data = ''
        if proc.returncode >= 0:
            try:
                lshw_data = json.loads(lshw_output.decode('utf8'))
            except Exception as e:
                lshw_data = lshw_output.decode('utf8')
                print('[EXCEPTION] LSHW exception', e, '\r')
            else:
                print('[INFO] LSHW successfully completed.', '\r')
        elif proc.returncode < 0:
            try:
                lshw_data = lshw_errors.decode('utf8')
            except Exception as e:
                lshw_data = str(e)
                print('[EXCEPTION]', e, '\r')
            else:
                print('[ERROR] LSHW failed execution with output: ', lshw_errors, '\r')
        # TODO verify it returns a dict object
        return lshw_data

    def get_dmi_data():
        """Get DMI table information using dmidecode command."""
        dmi_command = ['dmidecode']
        proc = subprocess.Popen(dmi_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        dmi_output, dmi_errors = proc.communicate()
        proc.wait()

        dmidecode_data = ''
        if proc.returncode >= 0:
            try:
                dmidecode_data = dmi_output.decode('utf8')
            except Exception as e:
                dmidecode_data = str(e)
                print('[EXCEPTION] DMIDECODE exception', e, '\r')
            else:
                print('[INFO] DMIDECODE successfully completed.', '\r')
        elif proc.returncode < 0:
            try:
                dmidecode_data = dmi_errors.decode('utf8')
            except Exception as e:
                dmidecode_data = str(e)
                print('[EXCEPTION] DMIDECODE exception', e, '\r')
            else:
                print('[ERROR] DMIDECODE failed execution with output: ', dmi_errors, '\r')

        # TODO verify it returns a string object
        return dmidecode_data

    def get_lspci_data():
        """Get hardware data using lspci command."""
        lspci_command = ['lspci -vv']
        proc = subprocess.Popen(lspci_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lspci_output, lspci_errors = proc.communicate()
        proc.wait()

        lspci_data = ''
        if proc.returncode >= 0:
            try:
                lspci_data = lspci_output.decode('utf8')
            except Exception as e:
                lspci_data = str(e)
                print('[EXCEPTION] LSPCI exception', e, '\r')
            else:
                print('[INFO] LSPCI successfully completed.', '\r')
        elif proc.returncode < 0:
            try:
                lspci_data = lspci_errors.decode('utf8')
            except Exception as e:
                lspci_data = str(e)
                print('[EXCEPTION] LSPCI exception', e, '\r')
            else:
                print('[ERROR] LSPCI failed execution with output: ', lspci_errors, '\r')
        # TODO verify it returns a string object
        return lspci_data

    def get_hwinfo_data():
        """Get hardware data using hwinfo command."""
        hwinfo_command = ['hwinfo --reallyall']
        proc = subprocess.Popen(hwinfo_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        hwinfo_output, hwinfo_errors = proc.communicate()
        proc.wait()

        hwinfo_data = ''
        if proc.returncode >= 0:
            try:
                hwinfo_data = hwinfo_output.decode('utf8')
            except Exception as e:
                hwinfo_data = str(e)
                print('[EXCEPTION] HWINFO exception', e, '\r')
            else:
                print('[INFO] HWINFO successfully completed.', '\r')
        elif proc.returncode < 0:
            try:
                hwinfo_data = hwinfo_errors.decode('utf8')
            except Exception as e:
                hwinfo_data = str(e)
                print('[EXCEPTION] HWINFO exception', e, '\r')
            else:
                print('[ERROR] HWINFO failed execution with output: ', hwinfo_errors, '\r')
        # TODO verify it returns a string object
        return hwinfo_data

    def get_smart_data():
        """Get smart data of disk using smartctl command."""
        # TODO validate if get NAME or KNAME of disks
        cmd_lsblk = ["lsblk -Jdo KNAME,TYPE"]
        proc = subprocess.Popen(cmd_lsblk, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output_lsblk, errors_lsblk = proc.communicate()
        proc.wait()

        try:
            disk_info = json.loads(output_lsblk.decode('utf8'))
        except Exception as e:
            print('[EXCEPTION] Detecting disks information', e)

        smart_data = []
        if proc.returncode == 0:
            for disk in disk_info['blockdevices']:
                if disk['type'] == 'disk':
                    smart_cmd = ["smartctl -x --json=csv /dev/" + disk['kname']]
                    proc_smart = subprocess.Popen(smart_cmd, shell=True, stdout=subprocess.PIPE,
                                                  stderr=subprocess.STDOUT)
                    smart_output, smart_errors = proc_smart.communicate()
                    proc_smart.wait()
                    # TODO improve disk data list with one key for disk
                    # TODO skip getting the usb disk where live iso was mounted
                    if proc_smart.returncode >= 0:
                        try:
                            disk_data = json.loads(smart_output.decode('utf8'))
                        except Exception as e:
                            smart_data.append(str(smart_output))
                            print('[EXCEPTION] SMART on', disk['kname'], 'exception', e)
                        else:
                            smart_data.append(disk_data)
                            print('[INFO] SMART on', disk['kname'], 'successfully completed.')
                    else:
                        print('[ERROR] SMART failed on', disk['kname'], 'with output:', smart_errors)
                        smart_data.append(str(smart_errors))
        else:
            print('[ERROR] Getting disks information failed with output:', errors_lsblk)
            return [errors_lsblk]
        # TODO verify it returns a list object
        return smart_data
