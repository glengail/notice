from sdk._platform.auth.auth import Authentication
from sdk._platform.app import Application
from sdk.dingtalk.auth.auth import DingtalkAuthentication
from sdk.dingtalk.client.client import DingtalkClient
class Dingtalk(Application):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Dingtalk, cls).__new__(cls, *args, **kwargs)
            cls.platform = 'dingtalk'
        return cls._instance

    def createClient(self, auth = None):
        return DingtalkClient(auth)
    
    @classmethod
    def newAuthentication(cls,appKey:str,appSecret:str)->Authentication:
        return DingtalkAuthentication(appKey,appSecret)
    
