import socket

from decouple import AutoConfig


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
