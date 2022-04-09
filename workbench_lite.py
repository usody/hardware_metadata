import json
import os
import subprocess
import uuid
from datetime import datetime

import requests


class WorkbenchLite:
    """ Create a hardware report of your computer with components using dmidecode package.
        You must run this software as root / sudo.
    """

    def __init__(self):
        if os.geteuid() != 0:
            raise EnvironmentError('[ERROR] Execute WorkbenchLite as root / sudo. \r')
        self.type = 'Snapshot'
        self.snapshot_uuid = uuid.uuid4()
        self.software = 'Workbench'
        self.version = '2022.03.3-alpha'

    def generate_wbid(self, uuid):
        from hashids import Hashids
        ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        # TODO short hash result to 6 characters
        return Hashids('', min_length=5, alphabet=ALPHABET).encode(uuid.time_mid)

    def get_lshw_data(self):
        """Get hw data using lshw command."""
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
                print('[INFO] LSHW successfully completed. \r')
        elif proc.returncode < 0:
            try:
                lshw_data = lshw_errors.decode('utf8')
            except Exception as e:
                lshw_data = str(e)
                print('[EXCEPTION]', e, '\r')
            else:
                print('[ERROR] LSHW failed execution with output: ', lshw_errors, '\r')

        return lshw_data

    def get_dmi_data(self):
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
                print('[INFO] DMIDECODE successfully completed. \r')
        elif proc.returncode < 0:
            try:
                dmidecode_data = dmi_errors.decode('utf8')
            except Exception as e:
                dmidecode_data = str(e)
                print('[EXCEPTION] DMIDECODE exception', e, '\r')
            else:
                print('[ERROR] DMIDECODE failed execution with output: ', dmi_errors, '\r')

        return dmidecode_data

    def get_lspci_data(self):
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
                print('[EXCEPTION] HWINFO exception', e, '\r')
            else:
                print('[INFO] HWINFO successfully completed. \r')
        elif proc.returncode < 0:
            try:
                lspci_data = lspci_errors.decode('utf8')
            except Exception as e:
                lspci_data = str(e)
                print('[EXCEPTION] HWINFO exception', e, '\r')
            else:
                print('[ERROR] HWINFO failed execution with output: ', lspci_errors, '\r')
        return lspci_data

    def get_hwinfo_data(self):
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
                print('[INFO] HWINFO successfully completed. \r')
        elif proc.returncode < 0:
            try:
                hwinfo_data = hwinfo_errors.decode('utf8')
            except Exception as e:
                hwinfo_data = str(e)
                print('[EXCEPTION] HWINFO exception', e, '\r')
            else:
                print('[ERROR] HWINFO failed execution with output: ', hwinfo_errors, '\r')
        return hwinfo_data

    def get_smart_data(self):
        """Get smart data of disk using smartctl command."""
        # TODO validate if get NAME or KNAME of disks
        cmd_lsblk = ["lsblk -Jdo KNAME,TYPE"]
        proc = subprocess.Popen(cmd_lsblk, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output_lsblk, errors_lsblk = proc.communicate()
        proc.wait()

        try:
            disk_info = json.loads(output_lsblk.decode('utf8'))
        except Exception as e:
            print('[EXCEPTION] Detecting disks information', e, '/r')

        smart_data = []
        if proc.returncode == 0:
            for disk in disk_info['blockdevices']:
                if disk['type'] == 'disk':
                    smart_cmd = ["smartctl -x --json=cosviu /dev/" + disk['kname']]
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
                            print('[EXCEPTION] SMART on', disk['kname'], 'exception', e, '\r')
                        else:
                            smart_data.append(disk_data)
                            print('[INFO] SMART on', disk['kname'], 'successfully completed. \r')
                    else:
                        print('[ERROR] SMART failed on', disk['kname'], 'with output:', smart_errors, '\r')
                        smart_data.append(str(smart_errors))
        else:
            print('[ERROR] Getting disks information failed with output:', errors_lsblk, '\r')
            return [errors_lsblk]

        return smart_data

    def generate_snapshot(self):
        """ Getting hardware data and generate snapshot file (json)."""

        # Generate WB ID base on snapshot uuid value
        wbid = self.generate_wbid(self.snapshot_uuid)
        print('[WBID]', wbid, '\r')

        snapshot_data = {}
        # Get hardware data and put it in snapshot
        snapshot_data.update({'lshw': self.get_lshw_data()})
        snapshot_data.update({'dmidecode': self.get_dmi_data()})
        snapshot_data.update({'lspci': self.get_lspci_data()})
        snapshot_data.update({'hwinfo': self.get_hwinfo_data()})
        snapshot_data.update({'smart': self.get_smart_data()})

        # Generate snapshot timestamp
        timestamp = datetime.now()

        # Generate and save snapshot
        snapshot = {
            'timestamp': timestamp,
            'type': 'Snapshot',
            'uuid': str(self.snapshot_uuid),
            'wbid': wbid,
            'software': str(self.software),
            'version': str(self.version),
            'data': snapshot_data
        }

        print('[INFO] Snapshot JSON successfully generated. \r')
        return snapshot


def save_snapshot(snapshot):
    timestamp = snapshot['timestamp'].strftime("%Y-%m-%d_%Hh%Mm%Ss")
    snapshot['timestamp'] = timestamp
    wbid = snapshot['wbid']
    json_file = '{date}_{wbid}_snapshot.json'.format(date=timestamp, wbid=wbid)
    with open(json_file, 'w') as file:
        json.dump(snapshot, file, indent=2, sort_keys=True)
    print('[INFO] Snapshot JSON successfully saved. \r')


def submit_snapshot(snapshot):
    domain = 'https://api.testing.usody.com'
    url = domain + '/api/inventory'
    token = 'ODY5ODRlZTgtYTdjOC00ZjdiLWE1NWYtYWMyNzdmYTlmMjQxOg=='

    post_headers = {'Authorization': 'Basic ' + token, 'Content-type': 'application/json'}
    snapshot['timestamp'] = str(snapshot['timestamp'])
    snapshot_json = json.dumps(snapshot)

    try:
        response = requests.post(url, headers=post_headers, data=snapshot_json)
        if response.status_code == 201:
            print('[INFO] Snapshot JSON successfully uploaded. \r')
            print('[INFO] Device page: ', domain + response.json()['device']['url'], '\r')
            return 0
        else:
            r = response.json()
            print('[ERROR] We could not auto-upload the device. Request error:',
                  r['code'], '-', r['type'], '-', r['message'], '\r')
            return r
    except Exception as e:
        print('[ERROR] Request exception:', e, '\r')
        return -1


if __name__ == '__main__':
    workbench_lite = WorkbenchLite()
    print('[INFO] ---- Starting Workbench ---- \r')
    print('[VERSION]', workbench_lite.version, '\r')
    snapshot = workbench_lite.generate_snapshot()
    save_snapshot(snapshot)
    submit_snapshot(snapshot)
    print('[INFO] ---- Workbench finished ---- \r')


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
