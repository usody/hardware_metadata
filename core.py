import os
import uuid
from datetime import datetime

from settings import Settings
from logs import Logs
from snapshot import Snapshot


class Core:
    """ Create a snapshot of your computer with hardware data and submit the information to a server.
        You must run this software as root / sudo.
    """

    def __init__(self):
        if os.geteuid() != 0:
            self.logs.error('Must be run as root / sudo.')
            exit(1)

        self.settings = Settings()
        self.timestamp = datetime.now()
        # Generate SID as an alternative id to the DHID when no internet
        self.snapshot_uuid = uuid.uuid4()
        self.sid = str(self.snapshot_uuid.time_mid).rjust(5, '0')
        self.logs = Logs.setup_logger(self.timestamp, self.sid)
        self.snapshot = Snapshot(self.timestamp, self.snapshot_uuid, self.sid, self.logs, self.settings)

    def print_snapshot_info(self):
        """Display on the screen relevant information about the tool."""
        self.logs.log(60, '  %s' % self.snapshot.version)
        self.logs.log(62, ' %s' % self.snapshot.settings_version)
        self.logs.log(64, '      %s' % self.snapshot.sid)

    def print_dh_info(self, r):
        """ Display on the screen relevant information about the DH."""
        self.logs.log(70, '    %s' % r['dhid'])
        self.logs.log(72, '   %s' % r['url'])
        self.logs.log(74, '   %s' % r['public_url'])

    def print_summary(self, json_file, response):
        """Display on the screen a summary of relevant information."""
        self.logs.info('=================== ( SUMMARY ) ===================')
        self.print_snapshot_info()
        self.logs.log(66, ' %s' % json_file)

        if response:
            r = response.json()
            if response.status_code == 201:
                self.print_dh_info(r)
        self.logs.info('Finished properly. You can press the power button to turn off.')
