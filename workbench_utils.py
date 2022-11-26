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

class WorkbenchLog:

    def setup_logger():
        """Return a logger with a default ColoredFormatter."""

        # To Define format - https://docs.python.org/3/library/stdtypes.html#printf-style-string-formatting
        formatter = ColoredFormatter(
            " %(log_color)s[%(levelname)s] %(message)s",
            datefmt=None,
            reset=True,
            log_colors={
                "VERSION": "bold_cyan",
                "SETTINGS": "bold_cyan",
                "SID": "bold_purple",
                "SNAPSHOT": "bold_purple",
                "DEBUG": "thin",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
            },
        )

        logging.addLevelName(60, "VERSION")
        logging.addLevelName(62, "SETTINGS")
        logging.addLevelName(64, "SID")
        logging.addLevelName(66, "SNAPSHOT")

        logger = logging.getLogger()
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        # Set which level logs display
        logger.setLevel(logging.INFO)

        return logger

    def print_run_info(self, wb):
        #wb.log.log(20,f"[VERSION] {wb.version}")
        #wb.log.log(20,"[VERSION] %(ver)s" % {'ver':wb.version})
        wb.log.log(60,"  %s" % wb.version)
        wb.log.log(62," %s" % wb.settings_version)
        wb.log.log(64,"      %s" % wb.sid)

    def print_summary(self, wb, json_file, response):
        print('-------------- [SUMMARY] --------------')
        self.print_run_info(wb)
        wb.log.log(66," %s" % json_file)

        if response:
            r = response.json()
            if response.status_code == 201:
                wb.log.info("DH_URL: %s" % r['url'])
                wb.log.log(20,"DH_ID: %s" % r['dhid'])
                wb.log.log(20,"DEVICE_URL: %s" % r['public_url'])
            else:
                wb.log.warning("We could not auto-upload the device. %s %s" % r['code'] % r['type'])
                wb.log.log(30,"Response: %s" % r['message'])
        
        
class DispatchingFormatter:
    """Dispatch formatter for logger and it's sub logger.
       Src: https://stackoverflow.com/a/34626685
    """
    def __init__(self, formatters, default_formatter):
        self._formatters = formatters
        self._default_formatter = default_formatter

    def format(self, record):
        # Search from record's logger up to it's parents:
        logger = logging.getLogger(record.name)
        while logger:
            # Check if suitable formatter for current logger exists:
            if logger.name in self._formatters:
                formatter = self._formatters[logger.name]
                break
            else:
                logger = logger.parent
        else:
            # If no formatter found, just use default:
            formatter = self._default_formatter
        return formatter.format(record)


class WorkbenchUtils:
    """ Collection of useful functions for the working of the tool. """

    def internet(host="8.8.8.8", port=53, timeout=3):
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
            print('[WARNING] No Internet.', ex.strerror)
            return False
