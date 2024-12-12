from urllib.parse import urlparse
from sdk._platform.notice.robot import OtoRobot as _OtoRobot
from sdk._platform.notice.robot import WebhookRobot as _WebhookRobot
from sdk._platform.notice.message import Message as _Message
from sdk.dingtalk.api.api_helper import SendOtoMessageResp, send_otoMessage,SendOtoMessageReq,send_groupMessage,SendWebhookMessageReq,PlatformResp
from sdk.dingtalk.notice.message import *
class Robot:
    @classmethod
    def createMessageWithText(cls,userids:list=None,content:str=None):
        msg = SampleText().setContent(content)
        msg.set_userIds(userids)
        return msg
    
    @classmethod
    def createMessageWithLink(cls,userids:list=None,text:str=None,pic_url:str=None,msg_url:str=None):
        msg = SampleLink().setText(text).setPicUrl(pic_url).setMessageUrl(msg_url)
        msg.set_userIds(userids)
        return msg
    
    @classmethod
    def createMessageWithMarkdown(cls,userids:list=None,title:str=None,text:str=None):
        msg = SampleMarkdown().setTitle(title).setText(text)
        msg.set_userIds(userids)
        return msg
    
    @classmethod
    def createMessageWithActionCard(cls,userids:list=None,title:str=None,text:str=None,singleTitle:str=None,singleUrl:str=None):
        msg = SampleActionCard().setTitle(title).setText(text).setSingleTitle(singleTitle).setSingleURL(singleUrl)
        msg.set_userIds(userids)
        return msg

class OtoRobot(_OtoRobot,Robot):
    def getRobotCode(self):
        return super().getId()
    
    def createMessageWithDefault(self, content, receivers = None):
        return self.createMessageWithText(userids=receivers, content=content)
    
    def send(self, message:_Message):
        return send_otoMessage(SendOtoMessageReq(
            access_token=self.auth.getAccessToken(),
            robotCode=self.getRobotCode(),
            userIds=message.get_userIds(),
            msgKey=message.getMsgType(),
            msgParam=message.getData(),
        ))
        
class GroupRobot(_WebhookRobot,Robot):

    @classmethod
    def createMessageWithText(cls,content = None):
        msg = Text().setContent(content)
        return msg
    
    @classmethod
    def createMessageWithLink(cls, text = None, pic_url = None, msg_url = None):
        msg = Link().setText(text).setPicUrl(pic_url).setMessageUrl(msg_url)
        return msg
    
    @classmethod
    def createMessageWithMarkdown(cls, title = None, text = None):
        msg = Markdown().setTitle(title).setText(text)
        return msg

    def createMessageWithDefault(self,content:str,receivers:list=None):
        return self.createMessageWithText( content=content)

    def send(self, message:_Message)->PlatformResp:
        parse_url = urlparse(self.getWebhook())
        if parse_url.netloc != 'oapi.dingtalk.com':
            return PlatformResp(errcode='200',errmsg=f'无效的webhook地址 {self.getWebhook()}')
        return send_groupMessage(SendWebhookMessageReq(
            url=self.getWebhook(),
            content={'msgtype':message.getMsgType(),message.getMsgType():message.getData()}
        ))