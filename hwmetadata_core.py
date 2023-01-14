import json
import os
import uuid
from datetime import datetime
from pathlib import Path

import requests
import socket

from hwmetadata_utils import HWMDSettings, HWMDUtils, HWMDLog
from hwmetadata_retrieval import HWMDRetrieval


class HWMDCore:
    """ Create a snapshot of your computer with hardware data and submit the information to a server.
        You must run this software as root / sudo.
    """

    def __init__(self):
        self.hwmd_utils = HWMDUtils()
        self.timestamp = datetime.now()
        # Generate SID as an alternative id to the DHID when no internet
        self.snapshot_uuid = uuid.uuid4()
        self.sid = self.generate_sid()
        self.log = HWMDLog.setup_logger(self.timestamp, self.sid)
        if os.geteuid() != 0:
            self.log.error('Must be run as root / sudo.')
            exit(1)
        
        self.type = 'Snapshot'
        self.software = 'Workbench'
        self.version = '2022.12.2-beta'
        self.schema_api = '1.0.0'

        self.dh_url = HWMDSettings.DH_URL
        self.dh_token = HWMDSettings.DH_TOKEN

        self.snapshots_path = HWMDSettings.SNAPSHOTS_PATH or os.getcwd()
        self.settings_version = HWMDSettings.VERSION or 'No Settings Version (NaN)'
       
    def generate_sid(self):
            return str(self.snapshot_uuid.time_mid).rjust(5, '0')

    def generate_snapshot(self):
        """ Getting hardware data and generate snapshot object."""
        snapshot_data = {}
        snapshot_data.update({'lshw': HWMDRetrieval.get_lshw_data(self.log)})
        snapshot_data.update({'dmidecode': HWMDRetrieval.get_dmi_data(self.log)})
        snapshot_data.update({'lspci': HWMDRetrieval.get_lspci_data(self.log)})
        # 2022-9-8: hwinfo is slow, it is in the stage of deprecation and it is not tested
        #   hence, don't run hwinfo on test situation
        #   info: disabling it reduces the process time from 17 to 2 seconds
        if(not os.environ.get("DISABLE_HWINFO")):
          snapshot_data.update({'hwinfo': HWMDRetrieval.get_hwinfo_data(self.log)})
        else:
          snapshot_data.update({'hwinfo': ''})
        snapshot_data.update({'smart': HWMDRetrieval.get_smart_data(self.log)})

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
            snapshots_folder=self.snapshots_path + '/snapshots/'
            Path(snapshots_folder).mkdir(parents=True, exist_ok=True)
            # Saving snapshot
            with open(snapshots_folder + json_file, 'w+') as file:
                json.dump(snapshot, file)
            self.log.info('Snapshot successfully saved on %s' % snapshots_folder)
            self.log.log(66,' %s' %json_file)
            return json_file
        except Exception as ex:
            self.log.error('Save snapshot: %s' % ex)
            self.log.debug('%s' % ex, exc_info=ex)
            return None

    def post_snapshot(self, snapshot):
        """ Upload snapshot to server."""
        if self.hwmd_utils.internet(self.log):
            if self.dh_url and self.dh_token:
                post_headers = {'Authorization': 'Basic ' + self.dh_token, 'Content-type': 'application/json'}

                try:
                    response = requests.post(self.dh_url, headers=post_headers, data=json.dumps(snapshot))
                    r = response.json()
                    if response.status_code == 201:
                        self.log.info('Snapshot JSON successfully uploaded.')
                        self.hwmd_utils.print_dh_info(self, r)
                    else:
                        self.log.warning('We could not auto-upload the device. {' + str(r['code']) + ' ' + str(r['type']) +'}')
                        self.log.debug(r['message'])
                    return response
                except Exception as ex:
                    self.log.error('POST snapshot exception:%s' % ex)
                    self.log.debug('%s' % ex, exc_info=ex)
                    return False
            else:
                self.log.warning('We could not auto-upload the device.')
                self.log.warning('Settings URL or TOKEN are empty.')
                self.log.warning('You can manually upload the snapshot.')
                return False


if '__main__' == __name__:
    hwmd_core = HWMDCore()

    print('------------------- [ STARTING HW METADATA ] -------------------')

    hwmd_core.hwmd_utils.print_hwmd_info(hwmd_core)

    step1 = '___________________(STEP 1:Generating Snapshot)_______________'
    print(step1)
    hwmd_core.log.debug('%s' %step1)
    snapshot = hwmd_core.generate_snapshot()

    step2 = '___________________(STEP 2:Saving Snapshot)___________________'
    print(step2)
    hwmd_core.log.debug('%s' %step2)    
    json_file = hwmd_core.save_snapshot(snapshot)

    step3 = '___________________(STEP 3:Uploading Snapshot)________________'
    print(step3)
    hwmd_core.log.debug('%s' %step3)
    response = hwmd_core.post_snapshot(snapshot)

    print('------------------- [ HW METADATA FINISHED ] -------------------')

    hwmd_core.hwmd_utils.print_summary(hwmd_core, json_file, response)
