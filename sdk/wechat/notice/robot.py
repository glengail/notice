from urllib.parse import urlparse
from sdk._platform.notice.message import Message as _Message
from sdk._platform.notice.robot import OtoRobot as _OtoRobot
from sdk._platform.notice.robot import WebhookRobot as _WebhookRobot
from sdk.wechat.notice.message import *
from sdk.wechat.api.api_helper import *

class Robot:
    @classmethod
    def createMessageWithText(self,userids:list=None,departmentids:list=None,tagids:list=None,content:str=None):
        msg = Text().setContent(content)
        msg.set_userIds(userids)
        msg.set_departmentIds(departmentids)
        msg.set_tagIds(tagids)
        return msg
    
    @classmethod
    def createMessageWithTextCard(self,userids:list=None,departmentids:list=None,tagids:list=None,title:str=None,desc:str=None,url:str=None,btntxt:str=None):
        msg = TextCard().setTitle(title).setDescription(desc).setUrl(url).setBtntxt(btntxt)
        msg.set_userIds(userids)
        msg.set_departmentIds(departmentids)
        msg.set_tagIds(tagids)
        return msg

class OtoRobot(_OtoRobot,Robot):
    def getAgentId(self):
        return super().getId()
    
    def createMessageWithDefault(self, content, receivers = None):
        return self.createMessageWithText(userids=receivers, content=content)

    def send(self,message:_Message):
        if not isinstance(message,Message):
            return SendOtoMessageResp(errcode='200',errmsg='Invalid message')
        #接收者是否为空
        if not message.hasReceivers():
            return SendOtoMessageResp(errcode='200',errmsg='接收者不能为空')
        return send_OtoMessage(SendOtoMessageReq(
                access_token=self.auth.getAccessToken(),
                agentid=self.getAgentId(),
                touser=message.get_formatedUserIds(),
                toparty=message.get_formatedDepartmentIds(),
                totag=message.get_formatedTagIds(),
                msgtype=message.getMsgType(),
                content=message.getData(),
                safe=message.get_safe(),
                enable_id_trans=message.get_enable_id_trans(),
                enable_duplicate_check=message.get_enable_duplicate_check(),
                duplicate_check_interval=message.get_duplicate_check_interval()
            ))
    

class GroupRobot(_WebhookRobot,Robot):

    def createMessageWithDefault(self,content:str):
        return self.createMessageWithText(content=content)

    def send(self, message:_Message)->PlatformResp:
        parse_url = urlparse(self.getWebhook())
        if parse_url.netloc != 'qyapi.weixin.qq.com':
            return PlatformResp(errcode='200',errmsg=f'无效的webhook地址 {self.getWebhook()}')
        return send_groupMessage(SendWebhookMessageReq(
            url=self.getWebhook(),
            content={'msgtype':message.getMsgType(),message.getMsgType():message.getData()}
        ))