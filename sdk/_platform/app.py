from abc import ABC, abstractmethod
from sdk._platform.auth import Authentication
from sdk._platform.client import Client
#平台抽象类，用户创建平台客户端实例
class Application(ABC):
    _instance = None
    platform = 'default'
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Application, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True

    @abstractmethod
    def createClient(self,auth:Authentication=None)->Client:
        pass

    @abstractmethod
    def newAuthentication(cls,key:str,secret:str)->Authentication:
        pass

