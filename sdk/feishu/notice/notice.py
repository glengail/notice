from sdk._platform.notice.notice import Notification
from sdk.feishu.notice.robot import OtoRobot,WebhookRobot
from sdk.feishu.auth.auth import FeishuAuthentication
class FeishuNotification(Notification):

    def __init__(self,auth:FeishuAuthentication):
        self.auth = auth

    def getOtoRobot(self, appid = None):
        return OtoRobot(self.auth)
    
    @classmethod
    def getWebhookRobot(cls, webhook_url):
        return WebhookRobot(webhook_url)
    