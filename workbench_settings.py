from decouple import AutoConfig


class WorkbenchSettings:
    # Path where find settings.ini file
    config = AutoConfig(search_path='/mnt/wb_settings/')

    # Env variables for DH parameters
    DH_TOKEN = config('DH_TOKEN', default='', cast=str)
    DH_URL = config('DH_URL', default='', cast=str)

    # Path where store snapshot files
    SNAPSHOT_PATH = config('SNAPSHOT_PATH', default='/mnt/snapshots/', cast=str)
