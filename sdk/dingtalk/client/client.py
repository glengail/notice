from sdk._platform import Client
from sdk.dingtalk.notice.notice import DingtalkNotification
class DingtalkClient(Client):
    def getNotification(self):
        if self.notification == None:
            self.notification = DingtalkNotification(super().getAuthentication())
        return self.notification