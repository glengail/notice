from abc import ABC,abstractmethod
from sdk._platform.auth import Authentication
from sdk._platform.notice import Notification
#平台客户端，用于管理各种功能(用户凭证、消息通知等)
class Client(ABC):
    def __init__(self,auth:Authentication):
        self.auth = auth
        self.notification = None
    
    def getAuthentication(self)->Authentication:
        return self.auth
    
    @abstractmethod
    def getNotification(self)->Notification:
        pass
