from abc import ABC,abstractmethod
from sdk._platform.auth.auth import Authentication
from sdk._platform.notice.robot import WebhookRobot,OtoRobot
#管理消息通知的方式，根据平台支持的方式修改
class Notification(ABC):
    def __init__(self,auth:Authentication):
        self.auth = auth
    
    #webhook机器人通知
    @classmethod
    def getWebhookRobot(cls,webhook_url:str)->WebhookRobot:
        return WebhookRobot(webhook_url)
    
    @abstractmethod
    def getOtoRobot(self,appid:str=None)->OtoRobot:
        pass
    
    