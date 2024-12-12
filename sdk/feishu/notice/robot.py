from urllib.parse import urlparse
from sdk._platform.notice.robot import OtoRobot as _OtoRobot
from sdk._platform.notice.robot import WebhookRobot as _WebhookRobot
from sdk._platform.notice.message import Message as _Message
from sdk.feishu.api.api_helper import *
from sdk.feishu.notice.message import *

class Robot:
    @classmethod
    def createMessageWithText(cls,userids:list=None,unionids:list=None,openids:list=None,departmentids:list=None,content:str=None):
        msg = Text().setText(content)
        msg.set_userIds(userids)
        msg.set_unionIds(unionids),
        msg.set_openIds(openids),
        msg.set_departmentIds(departmentids)
        return msg
    
class OtoRobot(_OtoRobot,Robot):
    
    def createMessageWithDefault(self, content, receivers = None):
        return self.createMessageWithText(userids=receivers, content=content)
        
    def send(self, message:_Message):
        if not isinstance(message,Message):
            return SendOtoMessageResp(errcode='200',errmsg='Invalid message')
        #接收者是否为空
        if not message.hasReceivers():
            return SendOtoMessageResp(errcode='200',errmsg='接收者为空')
        return sendOtoMessage(SendOtoMessageReq(
            accessToken=self.auth.getAccessToken(),
            msgType=message.getMsgType(),
            content=message.getData(),
            department_ids=message.get_departmentIds(),
            open_ids=message.get_openIds(),
            user_ids=message.get_userIds(),
            union_ids=message.get_unionIds(),
            card=None #未实现
        ))

class WebhookRobot(_WebhookRobot):
    
    @classmethod
    def createMessageWithDict(cls,data:dict=None):
        return DictData().setData(data)
    
    def createMessageWithDefault(cls, content):
        return cls.createMessageWithDict(data=content)
    
    def send(self, message:_Message)->PlatformResp:
        parse_url = urlparse(self.getWebhook())
        if parse_url.netloc != 'www.feishu.cn':
            return PlatformResp(errcode='200',errmsg=f'无效的webhook地址 {self.getWebhook()}')
        return send_groupMessage(SendWebhookMessageReq(
            url=self.getWebhook(),
            content=message.getData()
        ))
    