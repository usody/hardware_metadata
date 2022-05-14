from decouple import AutoConfig


class WorkbenchSettings:
    # Path where find settings.ini file
    config = AutoConfig(search_path='/root/wb/settings')

    # Env variables for DH parameters
    DH_TOKEN = config('DH_TOKEN', default='', cast=str)
    DH_DOMAIN = config('DH_DOMAIN', default='')
    DH_SCHEMA = config('DH_SCHEMA', default='')
    DH_URL = 'https://{domain}/{schema}/'.format(
        domain=DH_DOMAIN,
        schema=DH_SCHEMA
    )  # type: str

    # Path where store snapshot files
    WB_SNAPSHOT_PATH = config('WB_SNAPSHOT_PATH', default='/root/wb/snapshots/')