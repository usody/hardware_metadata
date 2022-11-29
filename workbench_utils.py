import socket
import logging

from decouple import AutoConfig
from colorlog import ColoredFormatter

class WorkbenchSettings:
    # Path where find settings.ini file
    config = AutoConfig(search_path='/mnt/wb_settings/')

    # Name of settings version
    VERSION = config('VERSION', default='', cast=str)

    # Env variables for DH parameters
    DH_TOKEN = config('DH_TOKEN', default='', cast=str)
    DH_URL = config('DH_URL', default='', cast=str)

    # Path where create snapshots folder
    SNAPSHOT_PATH = config('SNAPSHOT_PATH', default='', cast=str)


class HWMDLog:

    def setup_logger():
        """Return a logger with a default ColoredFormatter."""

        # To Define format - https://docs.python.org/3/library/stdtypes.html#printf-style-string-formatting
        formatter = ColoredFormatter(
            ' %(log_color)s[%(levelname)s] %(message)s',
            datefmt=None,
            reset=True,
            log_colors={
                'VERSION': 'bold_cyan',
                'SETTINGS': 'bold_cyan',
                'SID': 'bold_cyan',
                'SNAPSHOT': 'bold_cyan',
                'DH_ID': 'purple',
                'DH_URL': 'purple',
                'DEVICE': 'purple',
                'DEBUG': 'thin',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
            },
        )

        logging.addLevelName(60, 'VERSION')
        logging.addLevelName(62, 'SETTINGS')
        logging.addLevelName(64, 'SID')
        logging.addLevelName(66, 'SNAPSHOT')
        logging.addLevelName(70, 'DH_ID')
        logging.addLevelName(72, 'DH_URL')
        logging.addLevelName(74, 'DEVICE')

        logger = logging.getLogger()
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        # Set which level logs display
        logger.setLevel(logging.INFO)

        return logger
        

class WorkbenchUtils:
    """ A collection of useful functions for the correct working of the tool. """

    def print_hwmd_info(self, hwmd):
        """ Display on the screen relevant information about the tool. """
        hwmd.log.log(60, '  %s' % hwmd.version)
        hwmd.log.log(62, ' %s' % hwmd.settings_version)
        hwmd.log.log(64, '      %s' % hwmd.sid)

    def print_dh_info(self, hwmd, r):
        """ Display on the screen relevant information about the DH. """
        hwmd.log.log(70, '    %s' % r['dhid'])
        hwmd.log.log(72, '   %s' % r['url'])
        hwmd.log.log(74, '   %s' % r['public_url'])

    def print_summary(self, hwmd, json_file, response):
        """ Display on the screen a summary of relevant information. """
        hwmd.log.info('=================== ( SUMMARY ) ===================')
        self.print_hwmd_info(hwmd)
        hwmd.log.log(66, ' %s' % json_file)

        if response:
            r = response.json()
            if response.status_code == 201:
                self.print_dh_info(hwmd, r)
            else:
                hwmd.log.warning('We could not auto-upload the device. %s %s' % r['code'] % r['type'])
                # hwmd.log.warning('Response: %s' % r['message'])

    def internet(self, log, host='8.8.8.8', port=53, timeout=3):
        """
        Host: 8.8.8.8 (google-public-dns-a.google.com)
        OpenPort: 53/tcp
        Service: domain (DNS/TCP)
        Source: https://stackoverflow.com/a/33117579
        """
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except socket.error as ex:
            log.log.warning('No Internet', exc_info=ex)
            return False
