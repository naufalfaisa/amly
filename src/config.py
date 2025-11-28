import os
from dotenv import load_dotenv, set_key, unset_key, find_dotenv


class Configure(object):
    def __init__(self, config_dir: str = None):
        if config_dir is None:
            self.__env_file = ".env"
        else:
            self.__env_file = os.path.join(config_dir, ".env") if os.path.isdir(config_dir) or not config_dir.endswith('.env') else config_dir
        
        if os.path.exists(self.__env_file):
            load_dotenv(self.__env_file)
        else:
            with open(self.__env_file, 'w') as f:
                f.write("")
            
            __mediaUserToken = input("media-user-token: ")
            print()
            
            set_key(self.__env_file, "MEDIA_USER_TOKEN", __mediaUserToken)
            load_dotenv(self.__env_file)
    
    def get(self):
        load_dotenv(self.__env_file, override=True)
        return os.getenv("MEDIA_USER_TOKEN")
    
    def set(self):
        __mediaUserToken = input("media-user-token: ")
        print()
        set_key(self.__env_file, "MEDIA_USER_TOKEN", __mediaUserToken)
        os.environ["MEDIA_USER_TOKEN"] = __mediaUserToken
    
    def delete(self):
        unset_key(self.__env_file, "MEDIA_USER_TOKEN")
        if "MEDIA_USER_TOKEN" in os.environ:
            del os.environ["MEDIA_USER_TOKEN"]
