from sdk._platform.notice.message import Message as _Message
class SampleText(_Message):
    msgType = 'sampleText'
    def __init__(self):
        super().__init__()
    
    #设置文本内容
    def setContent(self,text:str):
        self.content = text
        return self
    
    def getContent(self):
        return self.content
    
    def getData(self):
        return str({'content':self.content})
    
class Text(SampleText):
    msgType = 'text'
    def __init__(self):
        super().__init__()
    
class SampleMarkdown(_Message):
    msgType = 'sampleMarkdown'
    def __init__(self):
        super().__init__()

    #设置标题
    def setTitle(self,title:str):
        self.title = title
        return self
    
    def getTitle(self):
        return self.title
    
    #设置文本内容
    def setText(self,text:str):
        self.text = text
        return self
    
    def getText(self):
        return self.text
    
    def getData(self):
        return str({'title':self.title, 'text':self.text})

class Markdown(SampleMarkdown):
    msgType = 'markdown'
    def __init__(self):
        super().__init__()

class SampleLink(_Message):
    msgType = 'sampleLink'
    def __init__(self):
        super().__init__()
    
    #设置文本内容
    def setText(self,text:str):
        self.text = text
        return self
    
    def getText(self):
        return self.text
    
    #设置点击跳转的URL
    def setMessageUrl(self,url:str):
        self.messageUrl = url
        return self
    
    def getMessageUrl(self):
        return self.messageUrl
    
    #设置图片URL
    def setPicUrl(self,url:str):
        self.picUrl = url
        return self
    
    def getPicUrl(self):
        return self.picUrl
    
    def getData(self):
        return str({'text':self.text, 'messageUrl':self.messageUrl, 'picUrl':self.picUrl})

class Link(SampleLink):
    msgType = 'link'
    def __init__(self):
        super().__init__()

class SampleActionCard(_Message):
    msgType = 'sampleActionCard'
    def __init__(self):
        super().__init__()
    
    #设置卡片的标题
    def setTitle(self,title:str):
        self.title = title
        return self
    
    #设置卡片的描述
    def setText(self,text:str):
        self.text = text
        return self
    
    #设置按钮的文字
    def setSingleTitle(self,singleTitle:str):
        self.singleTitle = singleTitle
        return self
    
    #设置跳转url
    def setSingleURL(self,singleUrl:str):
        self.singleURL = singleUrl
        return self
    
    def getData(self):
        return str({'title':self.title, 'text':self.text, 'singleTitle':self.singleTitle, 'singleURL':self.singleURL})
    
class ActionCard(SampleActionCard):
    msgType = 'actionCard'
    def __init__(self):
        super().__init__()