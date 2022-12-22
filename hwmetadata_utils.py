import os
import socket
import logging

from pathlib import Path
from decouple import AutoConfig
from colorlog import ColoredFormatter

class HWMDSettings:
    """Set of parameters to configure the correct working of the tool. """

    # Path where find settings.ini file
    config = AutoConfig(search_path='/mnt/hwmd_settings/')

    # Env variables for DH parameters
    DH_TOKEN = config('DH_TOKEN', default='', cast=str)
    DH_URL = config('DH_URL', default='', cast=str)

    # Path where create snapshots folder
    SNAPSHOTS_PATH = config('SNAPSHOTS_PATH', default='', cast=str)
    # Path where create logs folder
    LOGS_PATH = config('LOGS_PATH', default='', cast=str)

    # Name of settings version
    VERSION = config('VERSION', default='', cast=str)


class HWMDLog:

    def setup_logger(date, sid):
        """Return a logger with a custom ColoredFormatter."""

        # Customs log levels
        logging.addLevelName(60, 'VERSION')
        logging.addLevelName(62, 'SETTINGS')
        logging.addLevelName(64, 'SID')
        logging.addLevelName(66, 'SNAPSHOT')
        logging.addLevelName(70, 'DH_ID')
        logging.addLevelName(72, 'DH_URL')
        logging.addLevelName(74, 'DEVICE')

        custom_colors = {
                'VERSION': 'bold_cyan',
                'SETTINGS': 'bold_cyan',
                'SID': 'bold_cyan',
                'SNAPSHOT': 'bold_cyan',
                'DH_ID': 'purple',
                'DH_URL': 'purple',
                'DEVICE': 'purple',
                'DEBUG': '',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
            }

        # To Define format - https://docs.python.org/3/library/stdtypes.html#printf-style-string-formatting
        console_formatter = ColoredFormatter(
            ' %(log_color)s[%(levelname)s] %(message)s',
            datefmt=None,
            reset=True,
            log_colors=custom_colors,
        )

        file_formatter = ColoredFormatter(
            '%(asctime)s|%(log_color)s[%(levelname)s]%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            reset=True,
            log_colors=custom_colors,
        )

        logger = logging.getLogger('hwmd_log')
        logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        # Set which level logs display
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)

        # Return Path log file
        path_logfile = HWMDLog.setup_file_log(date, sid)

        file_handler = logging.FileHandler(path_logfile)
        file_handler.setFormatter(file_formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger

    def setup_file_log(date, sid):

        # Define name of log file
        log_filename = '{date}_{sid}_snapshot.log'.format(date=date.strftime("%Y-%m-%d_%Hh%Mm%Ss"),
                                                            sid=sid)
                                                            
        # Create logs folder
        logs_path = HWMDSettings.LOGS_PATH or os.getcwd()
        logs_folder = logs_path + '/logs/'
        Path(logs_folder).mkdir(parents=True, exist_ok=True)
        path_logfile = logs_folder + log_filename

        return path_logfile
        

class HWMDUtils:
    """A collection of useful functions for the correct working of the tool."""

    def print_hwmd_info(self, hwmd):
        """Display on the screen relevant information about the tool."""
        hwmd.log.log(60, '  %s' % hwmd.version)
        hwmd.log.log(62, ' %s' % hwmd.settings_version)
        hwmd.log.log(64, '      %s' % hwmd.sid)

    def print_dh_info(self, hwmd, r):
        """Display on the screen relevant information about the DH."""
        hwmd.log.log(70, '    %s' % r['dhid'])
        hwmd.log.log(72, '   %s' % r['url'])
        hwmd.log.log(74, '   %s' % r['public_url'])

    def print_summary(self, hwmd, json_file, response):
        """Display on the screen a summary of relevant information."""
        hwmd.log.info('=================== ( SUMMARY ) ===================')
        self.print_hwmd_info(hwmd)
        hwmd.log.log(66, ' %s' % json_file)

        if response:
            r = response.json()
            if response.status_code == 201:
                self.print_dh_info(hwmd, r)
        hwmd.log.info('Finished properly. You can press the power button to turn off.')

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
            log.warning('No Internet. %s' % ex)
            log.debug('%s' % ex, exc_info=ex)
            return False
