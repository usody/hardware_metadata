from decouple import AutoConfig


class WorkbenchSettings:
    # Path where find settings.ini file
    config = AutoConfig(search_path='/home/wb/settings')

    # Env variables for DH parameters
    DH_TOKEN = config('DH_TOKEN', default='')
    DH_URL = config('DH_URL', default='')

    # Path where store snapshot files
    WB_SNAPSHOT_PATH = config('WB_SNAPSHOT_PATH', default='/home/wb/snapshots/')
