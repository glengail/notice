from abc import ABC, abstractmethod
from sdk._platform.notice.receivers import Receivers

#消息类型定义，不同平台如果要增加更多消息类型实现该类即可
class Message(ABC,Receivers):
    msgType = ''
    def __init__(self):
        self.data = None
        super(Receivers,self).__init__()
    
    def _setData(self,data:any):
        self.data = data

    @abstractmethod
    def getData(self):
        pass

    @classmethod
    def getMsgType(cls)->str:
        return cls.msgType
