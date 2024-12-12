import requests
from sdk._platform.api.api_helper import *
def wechatRespHandle(resp:requests.models.Response):
    if resp.status_code != 200:
        return PlatformResp(str(resp.status_code),resp.reason)
    errcode = resp.json()['errcode']
    if errcode != 0 and errcode != '0':
        errmsg = resp.json()['errmsg']
        return PlatformResp(str(errcode),str(errmsg))
    return resp.json()

class GetAccessTokenReq:
    def __init__(self, corpid, corpsecret):
        self.corpid = corpid
        self.corpSecret = corpsecret
    def getCorpid(self):
        return self.corpid
    def getCorpsecret(self):
        return self.corpSecret
    
def get_AccessToken(req:GetAccessTokenReq)->GetAccessTokenResp:
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    params = {
        'corpid':req.getCorpid(),
        'corpsecret':req.getCorpsecret()
    }
    accesstoken = ''
    expires_in = '0'
    resp = wechatRespHandle(requests.get(url,params=params))
    if isinstance(resp,PlatformResp):
        return GetAccessTokenResp(accesstoken,expires_in,resp.getErrCode(),resp.getErrMsg())
    if 'access_token' in resp:
            accesstoken = resp['access_token']
    if 'expires_in' in resp:
            expires_in = resp['expires_in']
    return GetAccessTokenResp(accesstoken, expires_in)

class SendOtoMessageReq:
    def __init__(self, access_token:str,agentid:str,touser:str,toparty:str,totag:str,msgtype:str,content:any,safe:str,enable_id_trans:str,enable_duplicate_check:str,duplicate_check_interval:str):
        self.access_token = access_token
        self.agentid = agentid
        self.touser = touser
        self.toparty = toparty
        self.totag = totag
        self.msgtype = msgtype
        self.content = content
        self.safe = safe
        self.enable_id_trans = enable_id_trans
        self.enable_duplicate_check = enable_duplicate_check
        self.duplicate_check_interval = duplicate_check_interval

class SendOtoMessageResp(PlatformResp):
    def __init__(self,invaliduser='',invalidparty='',invalidtag='',errcode='0',errmsg='ok'):
        super().__init__(errcode,errmsg)
        self.invaliduser = invaliduser
        self.invalidparty = invalidparty
        self.invalidtag = invalidtag
    def getInvalidUser(self):
        return self.invaliduser
    def getInvalidParty(self):
        return self.invalidparty
    def getInvalidTag(self):
        return self.invalidtag
    
    def __str__(self):
            return f"SendOtoMessageResp(invaliduser='{self.invaliduser}', invalidparty='{self.invalidparty}', invalidtag='{self.invalidtag}', errcode='{self.errcode}', errmsg='{self.errmsg}')"
    
def send_OtoMessage(req:SendOtoMessageReq):
    url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send'
    params = {
        'access_token': req.access_token,
    }
    body = {
        "touser": req.touser, #接收消息的成员，成员ID列表（多个接收者用‘|’分隔，最多支持1000个） @all向该企业应用的全部成员发送
        "toparty": req.toparty, #指定接收消息的部门，部门ID列表，多个接收者用‘|’分隔，最多支持100个 @all忽略本参数
        "totag": req.totag, #指定接收消息的标签，标签ID列表，多个接收者用‘|’分隔，最多支持100个 @all忽略本参数
        "msgtype": req.msgtype, #消息类型
        "agentid": req.agentid,
        req.msgtype: req.content,
        "safe": req.safe, #是否是保密消息，0表示可对外分享，1表示不能分享且内容显示水印，默认为0
        "enable_id_trans": req.enable_id_trans, #是否开启id转译，0表示否，1表示是，默认
        "enable_duplicate_check": req.enable_duplicate_check ,#是否开启重复消息检查，0表示否，1表示是，默认0
        'duplicate_check_interval': req.enable_duplicate_check #'是否重复消息检查的时间间隔，默认1800s，最大不超过4小时'
    }
    invaliduser = invalidparty = invalidtag = ''
    resp = wechatRespHandle(requests.post(url=url,params=params,json=body))
    if isinstance(resp,PlatformResp):
        return SendOtoMessageResp(invaliduser, invalidparty, invalidtag, resp.getErrCode(), resp.getErrMsg())
    if 'invaliduser' in resp:
        invaliduser = resp['invaliduser']
    if 'invalidtag' in resp:
        invalidtag = resp['invalidtag']
    if 'invalidparty' in resp:
        invalidparty = resp['invalidparty']
    return SendOtoMessageResp(invaliduser, invalidparty, invalidtag)

def send_groupMessage(req:SendWebhookMessageReq):
    resp = wechatRespHandle(send_WebhookMessage(req))
    if isinstance(resp,PlatformResp):
        return resp
    return PlatformResp()