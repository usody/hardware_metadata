import os
import subprocess
import json
import uuid

from datetime import datetime


class WorkbenchLite:
    """ Create a hardware report of your computer with components using dmidecode package.
        You must run this software as root / sudo.
    """

    def __init__(self):
        if os.geteuid() != 0:
            raise EnvironmentError('[ERROR] Execute WorkbenchLite as root / sudo. \r')
        self.type = 'Snapshot'
        self.timestamp = datetime.now()
        self.snapshot_uuid = uuid.uuid4()
        self.software = 'WorkbenchLite'
        self.version = '2022.03'

    def generate_wbid(self, uuid: uuid):
        from hashids import Hashids
        ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        # TODO short hash result to 6 characters
        return Hashids('', min_length=5, alphabet=ALPHABET).encode(int(uuid))

    def get_dmi_data(self):
        """Get DMI table information using dmidecode command."""
        dmi_command = ['dmidecode']
        proc = subprocess.Popen(dmi_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        dmi_output, dmi_errors = proc.communicate()
        proc.wait()
        if proc.returncode < 0:
            print('[ERROR] DMIDECODE failed execution with output: ', dmi_errors, '\r')
            return str(dmi_errors.decode('utf8'))

        dmidecode_data = str(dmi_output.decode('utf8'))

        print('[INFO] DMIDECODE successfully completed. \r')
        return dmidecode_data

    def get_smart_data(self):
        """Execute dmidecode command."""
        # TODO validate if get NAME or KNAME of disks
        cmd_lsblk = ["lsblk -Jdo KNAME,TYPE"]
        proc = subprocess.Popen(cmd_lsblk, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output_lsblk, errors_lsblk = proc.communicate()
        proc.wait()
        disk_info = json.loads(str(output_lsblk.decode('utf8')))
        smart_data = []
        if proc.returncode >= 0:
            for disk in disk_info['blockdevices']:
                if disk['type'] == 'disk':
                    smart_cmd = ["smartctl -x --json=cosviu /dev/" + disk['kname']]
                    proc2 = subprocess.Popen(smart_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    output_smart, errors_smart = proc2.communicate()
                    proc2.wait()
                    if proc2.returncode < 0:
                        smart_data.append(str(errors_smart.decode('utf8')))
                    else:
                        smart_info = json.loads(str(output_smart.decode('utf8')))
                        smart_data.append(smart_info)
        else:
            print('[ERROR] SMARTCTL failed execution with output: ', errors_lsblk, '\r')
            return [errors_lsblk]
        print('[INFO] SMART successfully completed. \r')
        return smart_data

    def get_hwinfo_data(self):
        """Get DMI table information using dmidecode command."""
        hwinfo_command = ['hwinfo --reallyall']
        proc = subprocess.Popen(hwinfo_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        hwinfo_output, hwinfo_errors = proc.communicate()
        proc.wait()

        if proc.returncode < 0:
            print('[ERROR] HWINFO failed execution with output: ', hwinfo_errors, '\r')
            return str(hwinfo_errors.decode('utf8'))

        hwinfo_data = str(hwinfo_output.decode('utf8'))

        print('[INFO] HWINFO successfully completed. \r')
        return hwinfo_data

    def generate_snapshot(self):
        """ Getting hardware data and generate snapshot file (json)."""
        # Generate WB ID base on snapshot uuid value
        wbid = self.generate_wbid(self.snapshot_uuid)
        print('[INFO] | WBID | =', wbid, '\r')

        dmi_data = self.get_dmi_data()
        smart_data = self.get_smart_data()
        hwinfo_data = self.get_hwinfo_data()
        snapshot_data = {'dmidecode': dmi_data, 'hwinfo': hwinfo_data, 'smart': smart_data}

        snapshot = {
            'timestamp': str(self.timestamp),
            'type': 'Snapshot',
            'uuid': str(self.snapshot_uuid),
            'wbid': wbid,
            'software': 'WorkbenchLite',
            'version': str(self.version),
            'data': snapshot_data
        }

        # TODO change snapshot file name to {date}_{wbid}_WBv{version}...json
        with open('snapshot.json', 'w') as file:
            json.dump(snapshot, file)

        print('[INFO] Snapshot JSON successfully saved. \r')


if __name__ == '__main__':
    workbench_lite = WorkbenchLite()
    print('[INFO] Starting WBv14! \r')
    workbench_lite.generate_snapshot()
    print('[INFO] Finished WBv14! \r')


# Funciton to convert an int32 to an alphanumeric ID of 6 characters
# Src: https://stackoverflow.com/questions/51333374/shortest-possible-generated-unique-id
def int32_to_id(n):
    if n == 0: return "0"
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    length = len(chars)
    result = ""
    remain = n
    while remain > 0:
        pos = remain % length
        remain = remain // length
        result = chars[pos] + result
    return result
