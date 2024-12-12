from sdk._platform.auth.auth import Authentication
from sdk._platform.app import Application
from sdk.wechat.auth.auth import WechatAuthentication
from sdk.wechat.client.client import WechatClient

class Wechat(Application):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Wechat, cls).__new__(cls, *args, **kwargs)
            cls.platform = 'wechat'
        return cls._instance

    @classmethod
    def createClient(cls, auth:Authentication):
        return WechatClient(auth)
    
    @classmethod
    def newAuthentication(cls, corpId:str,corpSecret:str)->Authentication:
        return WechatAuthentication(corpId,corpSecret)
    
    