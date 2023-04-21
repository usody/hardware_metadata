import os
import uuid
from datetime import datetime

# Allow to use the code as a module
try:
    from settings import Settings
    from logs import Logs
    from snapshot import Snapshot
except ModuleNotFoundError:
    import sys
    import pathlib
    sys.path.append(
        pathlib.Path(__file__).parent.parent.absolute().as_posix()
    )
    from hardware_metadata.settings import Settings
    from hardware_metadata.logs import Logs
    from hardware_metadata.snapshot import Snapshot


class Core:
    """ Create a snapshot of your computer with hardware data and submit the information to a server.
        You must run this software as root / sudo.
    """

    def __init__(self, software, software_version):
        if os.geteuid() != 0:
            self.logs.error('Must be run as root / sudo.')
            exit(1)

        self.settings = Settings()
        self.timestamp = datetime.now()
        # Generate SID as an alternative id to the DHID when no internet
        self.snapshot_uuid = uuid.uuid4()
        self.sid = str(self.snapshot_uuid.time_mid).rjust(5, '0')
        self.logs = Logs.setup_logger(self.timestamp, self.sid)
        self.software = software
        self.software_version = software_version
        self.snapshot = Snapshot(self.timestamp, self.snapshot_uuid, self.sid, self.software, self.software_version, self.logs, self.settings)

    def print_snapshot_info(self):
        """Display on the screen relevant information about the tool."""
        self.logs.log(60, '  %s' % self.snapshot.software_version)
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
