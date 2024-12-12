from sdk._platform.auth import Authentication
from sdk._platform.app import Application
from sdk.feishu.client.client import FeishuClient
from sdk.feishu.auth.auth import FeishuAuthentication
class Feishu(Application):
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Feishu,cls).__new__(cls, *args, **kwargs)
            cls.platform = 'feishu'
        return cls._instance
    
    @classmethod
    def newAuthentication(cls, appID:str, appSecret:str)->Authentication:
        return FeishuAuthentication(appID,appSecret)
    
    @classmethod
    def createClient(cls, auth:Authentication):
        return FeishuClient(auth)
    
