from decouple import AutoConfig

class Settings:
    """Set of parameters to configure the correct working of the tool. """

    # Path where find settings.ini file
    config = AutoConfig(search_path='/mnt/settings/')

    # Env variables for DH parameters
    DH_TOKEN = config('DH_TOKEN', default='', cast=str)
    DH_URL = config('DH_URL', default='', cast=str)

    # Path where create snapshots folder
    SNAPSHOTS_PATH = config('SNAPSHOTS_PATH', default='', cast=str)
    # Path where create logs folder
    LOGS_PATH = config('LOGS_PATH', default='', cast=str)

    # Name of settings version
    SETTINGS_VERSION = config('SETTINGS_VERSION', default='', cast=str)

    SOFTWARE = config('SOFTWARE', default='', cast=str)
    SOFTWARE_VERSION = config('SOFTWARE_VERSION', default='', cast=str)