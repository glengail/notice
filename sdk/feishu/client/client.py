from sdk._platform import Client
from sdk.feishu.notice.notice import FeishuNotification
class FeishuClient(Client):
    def getNotification(self):
        if self.notification == None:
            self.notification = FeishuNotification(self.auth)
        return self.notification