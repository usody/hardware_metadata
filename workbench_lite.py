import json
import os
import subprocess
import uuid
from datetime import datetime

import requests


class WorkbenchLite:
    """ Create a snapshot of your computer with hardware data and submit the information to a server.
        You must run this software as root / sudo.
    """

    def __init__(self):
        if os.geteuid() != 0:
            raise EnvironmentError('[ERROR] Execute WorkbenchLite as root / sudo. \r')
        self.type = 'Snapshot'
        self.snapshot_uuid = uuid.uuid4()
        self.software = 'Workbench'
        self.version = '2022.4.0-beta'
        self.schema_api = '1.0.0'

    def generate_sid(self, uuid):
        from hashids import Hashids
        ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        # TODO short hash result to 6 characters
        return Hashids('', min_length=5, alphabet=ALPHABET).encode(uuid.time_mid)

    def get_lshw_data(self):
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
                print('[INFO] LSHW successfully completed. \r')
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

        # TODO verify it returns a string object
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
                print('[EXCEPTION] LSPCI exception', e, '\r')
            else:
                print('[INFO] LSPCI successfully completed. \r')
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
        # TODO verify it returns a string object
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
        # TODO verify it returns a list object
        return smart_data

    def generate_snapshot(self):
        """ Getting hardware data and generate snapshot file (json)."""

        # Generate WB ID base on snapshot uuid value
        sid = self.generate_sid(self.snapshot_uuid)
        print('[SNAPSHOT ID]', sid, '\r')

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
            'timestamp': timestamp.isoformat(),
            'type': 'Snapshot',
            'uuid': str(self.snapshot_uuid),
            'sid': sid,
            'software': self.software,
            'version': self.version,
            'schema_api': self.schema_api,
            'data': snapshot_data
        }

        print('[INFO] Snapshot JSON successfully generated. \r')
        return snapshot, timestamp


def save_snapshot(snapshot, timestamp):
    try:
        json_file = '{date}_{sid}_snapshot.json'.format(date=timestamp.strftime("%Y-%m-%d_%Hh%Mm%Ss"),
                                                        sid=snapshot['sid'])
        with open(json_file, 'w') as file:
            json.dump(snapshot, file, indent=2, sort_keys=True)
        return 0
    except Exception as e:
        print('[ERROR] Save snapshot exception:', e, '\r')
        return e


def post_snapshot(snapshot):
    domain = 'https://api.testing.usody.com'
    url = domain + '/api/inventory/'
    token = 'ODY5ODRlZTgtYTdjOC00ZjdiLWE1NWYtYWMyNzdmYTlmMjQxOg=='

    post_headers = {'Authorization': 'Basic ' + token, 'Content-type': 'application/json'}
    snapshot['timestamp'] = str(snapshot['timestamp'])
    snapshot_json = json.dumps(snapshot)

    try:
        response = requests.post(url, headers=post_headers, data=snapshot_json)
        r = response.json()
        if response.status_code == 201:
            print('[INFO] Snapshot JSON successfully uploaded. \r')
            print('[INFO] Device URL: ', domain + r['url'], '\r')
        if response.status_code == 400:
            print('[ERROR] We could not auto-upload the device. \r')
            print('Response error:', r, '\r')
        else:
            print('[WARNING] Response error:', r['code'], '-', r['type'], '\r')
            print(r['message'][0], '\r')
        return r
    except Exception as e:
        print('[EXCEPTION] Post snapshot exception:', e, '\r')
        return e


if '__main__' == __name__:
    workbench_lite = WorkbenchLite()

    print('[INFO] ---- Starting Workbench ---- \r')
    print('[VERSION]', workbench_lite.version, '\r')

    snapshot, timestamp = workbench_lite.generate_snapshot()

    rsave = save_snapshot(snapshot, timestamp)
    if rsave == 0:
        print('[INFO] Snapshot JSON successfully saved. \r')
    else:
        print('[EXCEPTION] Save exception:', rsave, '\r')

    post_snapshot(snapshot)

    print('[INFO] ---- Workbench finished ---- \r')
