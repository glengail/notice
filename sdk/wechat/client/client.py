from sdk.wechat.auth.auth import Authentication
from sdk.wechat.notice.notice import WechatNotification
from sdk._platform.client.client import Client
class WechatClient(Client):
    def getNotification(self):
        if self.notification is None:
            self.notification = WechatNotification(self.auth)
        return self.notification
    
    