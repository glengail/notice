from sdk.wechat.notice.receivers import Receivers
from sdk.wechat.notice.utils.format_helper import list2FormattedIds
from sdk._platform.notice.message import Message as _Message

class Message(Receivers,_Message):
        
    def __init__(self):
        super().__init__()
        super(Receivers).__init__()
        self.receivers = None
        self.content = None
        self.init_Others()
    
    def init_Others(self):
        self.safe = 0
        self.enable_id_trans = 0
        self.enable_duplicate_check = 0
        self.duplicate_check_interval = 1800

    #表示是否是保密消息，0表示可对外分享，1表示不能分享且内容显示水印，默认为0
    def set_safe(self, value):
        self.safe = value

    #表示是否开启id转译，0表示否，1表示是，默认0。
    def set_enable_id_trans(self, value):
        self.enable_id_trans = value
    
    #表示是否开启重复消息检查，0表示否，1表示是，默认0
    def set_enable_duplicate_check(self, value):
        self.enable_duplicate_check = value

    #表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时
    def set_duplicate_check_interval(self, value):
        self.duplicate_check_interval = value

    def get_safe(self):
        return self.safe
    
    def get_enable_id_trans(self):
        return self.enable_id_trans
    
    def get_enable_duplicate_check(self):
        return self.enable_duplicate_check
    
    def get_duplicate_check_interval(self):
        return self.duplicate_check_interval
    
class Text(Message):
    msgType = 'text'
    def __init__(self):
        super().__init__()
    
    #设置文本内容
    def setContent(self,text:str):
        self.content = text
        return self
    
    def getData(self):
        return {'content':self.content}

#文本卡片消息
class TextCard(Message):
    msgType = 'textcard'
    def __init__(self):
        super().__init__()
        self.title = ''
        self.description = ''
        self.url = ''
        self.btntxt = ''
       #self._setData({'title': self.getTitle(), 'description': self.getDescription(), 'url': self.getUrl(), 'btntxt': self.getBtntxt()})
    
    def getData(self):
        return {'title': self.getTitle(), 'description': self.getDescription(), 'url': self.getUrl(), 'btntxt': self.getBtntxt()}
    
    #设置标题
    def setTitle(self,title:str):
        self.title = title
        return self
    
    def getTitle(self):
        return self.title
    
    #设置描述
    def setDescription(self,description:str):
        self.description = description
        return self
    
    def getDescription(self):
        return self.description
    
    #点击后跳转的链接。最长2048字节，请确保包含了协议头(http/https)
    def setUrl(self,url:str):
        self.url = url
        return self
    
    def getUrl(self):
        return self.url
    
    #按钮文字。 默认为“详情”， 不超过4个文字，超过自动截断。
    def setBtntxt(self,btntxt:str):
        self.btntxt = btntxt
        return self
    
    def getBtntxt(self):
        return self.btntxt
    

            


