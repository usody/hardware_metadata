import json
import os
import uuid
from datetime import datetime
from pathlib import Path

import requests
import socket

from workbench_utils import WorkbenchSettings, WorkbenchUtils, HWMDLog
from workbench_hwdata import HardwareData


class WorkbenchCore:
    """ Create a snapshot of your computer with hardware data and submit the information to a server.
        You must run this software as root / sudo.
    """

    def __init__(self):
        self.log = HWMDLog.setup_logger()
        if os.geteuid() != 0:
            self.hwmd_log.error('Execute Workbench as root / sudo.')
            exit(1)
        self.timestamp = datetime.now()
        self.type = 'Snapshot'
        self.snapshot_uuid = uuid.uuid4()
        self.software = 'Workbench'
        self.version = '2022.11.3-beta'
        self.schema_api = '1.0.0'
        # Generate SID as an alternative id to the DHID when no internet 
        self.sid = self.generate_sid()
        self.dh_url = WorkbenchSettings.DH_URL
        self.dh_token = WorkbenchSettings.DH_TOKEN
        self.snapshots_path = WorkbenchSettings.SNAPSHOT_PATH or os.getcwd()
        self.settings_version = WorkbenchSettings.VERSION or 'No Settings Version (NaN)'
       
    def generate_sid(self):
            return str(self.snapshot_uuid.time_mid).rjust(5, '0')

    def generate_snapshot(self):
        """ Getting hardware data and generate snapshot object."""
        snapshot_data = {}
        snapshot_data.update({'lshw': HardwareData.get_lshw_data(self.log)})
        snapshot_data.update({'dmidecode': HardwareData.get_dmi_data(self.log)})
        snapshot_data.update({'lspci': HardwareData.get_lspci_data(self.log)})
        # 2022-9-8: hwinfo is slow, it is in the stage of deprecation and it is not tested
        #   hence, don't run hwinfo on test situation
        #   info: disabling it reduces the process time from 17 to 2 seconds
        if(not os.environ.get("DISABLE_HWINFO")):
          snapshot_data.update({'hwinfo': HardwareData.get_hwinfo_data(self.log)})
        else:
          snapshot_data.update({'hwinfo': ''})
        snapshot_data.update({'smart': HardwareData.get_smart_data(self.log)})

        # Generate snapshot
        snapshot = {
            'timestamp': self.timestamp.isoformat(),
            'type': self.type,
            'uuid': str(self.snapshot_uuid),
            'sid': self.sid,
            'software': self.software,
            'version': self.version,
            'schema_api': self.schema_api,
            'settings_version': self.settings_version,
            'data': snapshot_data
        }
        self.log.info('Snapshot generated properly.')
        return snapshot

    def save_snapshot(self, snapshot):
        """ Save snapshot like JSON file on local storage."""
        try:
            json_file = '{date}_{sid}_snapshot.json'.format(date=self.timestamp.strftime("%Y-%m-%d_%Hh%Mm%Ss"),
                                                            sid=self.sid)
            # Create snapshots folder
            snapshot_folder=self.snapshots_path + '/snapshots/'
            Path(snapshot_folder).mkdir(parents=True, exist_ok=True)
            # Saving snapshot
            with open(snapshot_folder + json_file, 'w+') as file:
                json.dump(snapshot, file)
            self.log.info('Snapshot successfully saved on %s' % snapshot_folder)
            self.log.log(66,' %s' %json_file)
            return json_file
        except Exception as e:
            self.log.error('Save snapshot:',exc_info=e)
            return None

    def post_snapshot(self, snapshot):
        """ Upload snapshot to server."""
        if hwmd_utils.internet(self.log):
            if self.dh_url and self.dh_token:
                post_headers = {'Authorization': 'Basic ' + self.dh_token, 'Content-type': 'application/json'}

                try:
                    response = requests.post(self.dh_url, headers=post_headers, data=json.dumps(snapshot))
                    r = response.json()
                    if response.status_code == 201:
                        self.log.info('Snapshot JSON successfully uploaded.')
                        hwmd_utils.print_dh_info(self, r)
                    elif response.status_code == 400:
                        self.log.error('We could not auto-upload the device. {' + str(response.status_code) + ' ' + str(response.reason)+'}')
                        self.log.error('Response error: %s' % r)
                    else:
                        self.log.warning('We could not auto-upload the device. {' + str(r['code']) + ' ' + str(r['type']) +'}')
                        self.log.warning('Response: %s' % r['message']) 
                    return response
                except Exception as e:
                    self.log.error('POST snapshot exception:', exc_info=e)
                    return False
            else:
                self.log.warning('We could not auto-upload the device. Settings URL or TOKEN are empty.')
                return False


if '__main__' == __name__:
    workbench_core = WorkbenchCore()
    hwmd_utils = WorkbenchUtils()

    print('----------------- [ STARTING HW METADATA ] -----------------')

    hwmd_utils.print_hwmd_info(workbench_core)

    workbench_core.log.info('|____________STEP 1:Generating Snapshot____________|')
    snapshot = workbench_core.generate_snapshot()

    workbench_core.log.info('|____________STEP 2:Saving Snapshot________________|')    
    json_file = workbench_core.save_snapshot(snapshot)

    workbench_core.log.info('|____________STEP 3:Uploading Snapshot_____________|')
    response = workbench_core.post_snapshot(snapshot)

    print('----------------- [ HW METADATA FINISHED ] -----------------')

    hwmd_utils.print_summary(workbench_core, json_file, response)
