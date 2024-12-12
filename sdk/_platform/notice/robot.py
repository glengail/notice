from abc import ABC, abstractmethod
from sdk._platform.notice.message import Message
from sdk._platform.auth.auth import Authentication
from sdk._platform.api.api_helper import PlatformResp
#消息通知方式的实现
class OtoRobot(ABC):
    def __init__(self,auth:Authentication,id:str=None):
        self.auth = auth
        self.id = id
    
    @abstractmethod
    def createMessageWithDefault(self,content:str,receivers:list=None)->Message:
        pass
    
    def getId(self):
        return self.id
    
    @abstractmethod
    def send(self,message:Message)->PlatformResp:
        pass

class WebhookRobot(ABC):
    @abstractmethod
    def createMessageWithDefault(self,content:str):
        pass

    def __init__(self,webhook_url:str):
        self.webhook_url = webhook_url

    def setWebhook(self,url:str):
        self.webhook_url = url

    def getWebhook(self)->str:
        return self.webhook_url
    
    @abstractmethod
    def send(self,message:Message)->PlatformResp:
        pass