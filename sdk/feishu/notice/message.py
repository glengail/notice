from sdk._platform.notice.message import Message as _Message
from sdk.feishu.notice.receivers import Receivers

class Message(Receivers,_Message,):
    def __init__(self):
        super().__init__()
        super(Receivers).__init__()

    #调Receivers的
    def hasReceivers(self)->bool:
        return super().hasReceivers()
    
class Text(Message):
    msgType = 'text'
    def __init__(self):
        super().__init__()
    
    #设置文本内容
    def setText(self, text):
        self.text = text
        return self
    
    def getText(self):
        return self.text
    
    def getData(self):
        return {'text':self.getText()}
    
class DictData(Message):

    msgType = 'dict'

    def __init__(self):
        super().__init__()

    def setData(self,data:dict):
        self.data = data
        return self

    def getData(self):
        return self.data
    
    