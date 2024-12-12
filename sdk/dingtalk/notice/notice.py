from sdk._platform.notice.notice import Notification
from sdk.dingtalk.auth.auth import DingtalkAuthentication
from sdk.dingtalk.notice.robot import OtoRobot,GroupRobot
class DingtalkNotification(Notification):
    def __init__(self,auth:DingtalkAuthentication):
        self.auth = auth
    
    #批量发送单聊消息
    def getOtoRobot(self, appid = None):
        return OtoRobot(self.auth,self.auth.getKey())
    
    #发送群聊消息
    @classmethod
    def getGroupRobot(cls,webhook_url:str):
        return GroupRobot(webhook_url)
    
    @classmethod
    def getWebhookRobot(cls, webhook_url):
        return GroupRobot(webhook_url)