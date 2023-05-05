import os
import socket
import logging

from pathlib import Path
from colorlog import ColoredFormatter

try:
    from settings import Settings
except ModuleNotFoundError:
    import sys
    import pathlib
    sys.path.append(
        pathlib.Path(__file__).parent.parent.absolute().as_posix()
    )
    from hardware_metadata.settings import Settings


class Logs:

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

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        # Set which level logs display
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)

        # Return Path log file
        path_logfile = Logs.setup_file_log(date, sid)

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
        logs_path = Settings.LOGS_PATH or os.getcwd()
        logs_folder = logs_path + '/logs/'
        Path(logs_folder).mkdir(parents=True, exist_ok=True)
        path_logfile = logs_folder + log_filename

        return path_logfile

