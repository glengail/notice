from sdk._platform.notice.notice import Notification
from sdk.wechat.notice.robot import OtoRobot,GroupRobot
from sdk.wechat.auth.auth import WechatAuthentication
class WechatNotification(Notification):
    def __init__(self,auth:WechatAuthentication):
        self.auth = auth

    def getOtoRobot(self, appid = None):
        return OtoRobot(self.auth, appid)

    @classmethod
    def getGroupRobot(cls,webhook_url:str):
        return GroupRobot(webhook_url)
    
    @classmethod
    def getWebhookRobot(cls, webhook_url):
        return GroupRobot(webhook_url)
    



    
    


