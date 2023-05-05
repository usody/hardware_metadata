import json
import os
import requests
import socket

from pathlib import Path

try:
    from hw_retrieval import HWMD
except ModuleNotFoundError:
    import sys
    sys.path.append(Path(__file__).parent.parent.absolute().as_posix()
    )
    from hardware_metadata.hw_retrieval import HWMD



class Snapshot():
    """ Create a snapshot of your computer with hardware data and submit the information to a server.
        You must run this software as root / sudo.
    """

    def __init__(self, timestamp, snapshot_uuid, sid, software, software_version, logs, settings):
        self.timestamp = timestamp
        # Generate SID as an alternative id to the DHID when no internet
        self.snapshot_uuid = snapshot_uuid
        self.sid = sid
        self.logs = logs

        self.type = 'Snapshot'
        self.software = software
        self.software_version = software_version
        self.schema_api = '1.0.0'

        self.dh_url = settings.DH_URL
        self.dh_token = settings.DH_TOKEN

        self.snapshots_path = settings.SNAPSHOTS_PATH or os.getcwd()
        self.settings_version = settings.SETTINGS_VERSION or 'No Settings Version (NaN)'

    def generate_snapshot(self):
        """ Getting hardware data and generate snapshot object."""
        hw_data = {}
        hw_data.update({'hwmd_version': self.software_version})
        hw_data.update({'lshw': HWMD.get_lshw_data(self.logs)})
        hw_data.update({'dmidecode': HWMD.get_dmi_data(self.logs)})
        hw_data.update({'lspci': HWMD.get_lspci_data(self.logs)})
        # 2022-9-8: hwinfo is slow, it is in the stage of deprecation and it is not tested
        #   hence, don't run hwinfo on test situation
        #   info: disabling it reduces the process time from 17 to 2 seconds
        if(not os.environ.get("DISABLE_HWINFO")):
          hw_data.update({'hwinfo': HWMD.get_hwinfo_data(self.logs)})
        else:
          hw_data.update({'hwinfo': ''})
          
        tests_data = {'smart': HWMD.get_smart_data(self.logs)}

        # Generate snapshot
        snapshot = {
            'timestamp': self.timestamp.isoformat(),
            'type': self.type,
            'uuid': str(self.snapshot_uuid),
            'sid': self.sid,
            'software': self.software,
            'version': self.software_version,
            'schema_api': self.schema_api,
            'settings_version': self.settings_version,
            'hwmd': hw_data,
            'tests': tests_data
        }
        self.logs.info('Snapshot generated properly.')
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
            self.logs.info('Snapshot successfully saved on %s' % snapshots_folder)
            self.logs.log(66,' %s' %json_file)
            return json_file
        except Exception as ex:
            self.logs.error('Save snapshot: %s' % ex)
            self.logs.debug('%s' % ex, exc_info=ex)
            return None

    def post_snapshot(self, snapshot):
        """ Upload snapshot to server."""
        # TODO: remove internet() and catch request Exceptions: Connection and Timeout
        self.internet()
        if self.dh_url and self.dh_token:
            post_headers = {'Authorization': 'Basic ' + self.dh_token, 'Content-type': 'application/json'}

            try:
                response = requests.post(self.dh_url, headers=post_headers, data=json.dumps(snapshot))
                r = response.json()
                if response.status_code == 201:
                    self.logs.info('Snapshot JSON successfully uploaded.')
                    # Display on the screen relevant information about the DH
                    self.logs.log(70, '    %s' % r['dhid'])
                    self.logs.log(72, '   %s' % r['url'])
                    self.logs.log(74, '   %s' % r['public_url']) 
                else:
                    self.logs.warning('We could not auto-upload the device. {' + str(r['code']) + ' ' + str(r['type']) +'}')
                    self.logs.debug(r['message'])
                return response
            except Exception as ex:
                self.logs.warning('We could not auto-upload the device.')
                self.logs.warning('You can manually upload the snapshot.')
                self.logs.debug('POST snapshot exception: %s' % ex)
                return False
        else:
            self.logs.warning('We could not auto-upload the device.')
            self.logs.warning('Settings URL or TOKEN are empty.')
            self.logs.warning('You can manually upload the snapshot.')
            return False

    def internet(self, host='8.8.8.8', port=53, timeout=3):
        """
        Host: 8.8.8.8 (google-public-dns-a.google.com)
        OpenPort: 53/tcp
        Service: domain (DNS/TCP)
        Source: https://stackoverflow.com/a/33117579
        """
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        except socket.error as ex:
            self.logs.warning('No Internet. %s' % ex)
            self.logs.debug('%s' % ex, exc_info=ex)
