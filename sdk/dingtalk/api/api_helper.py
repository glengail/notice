import requests
from sdk._platform.api.api_helper import PlatformResp,GetAccessTokenResp,SendWebhookMessageReq,send_WebhookMessage
def dingtalkRespHandle(res:requests.models.Response):
    if 'code' in res.json() and 'message' in res.json():
        return PlatformResp(str(res.json()['code']),str(res.json()['message']))
    if 'errcode' in res.json() and res.json()['errcode'] != 0:
        return PlatformResp(str(res.json()['errcode']),str(res.json()['errmsg']))
    if res.status_code != 200:
        return PlatformResp(str(res.status_code),res.reason)
    return res.json()

class GetAccessTokenReq:
    def __init__(self, appKey:str, appSecret:str):
        self.appKey = appKey
        self.appSecret = appSecret

    def getAppkey(self):
        return self.appKey
    
    def getAppSecret(self):
        return self.appSecret
    
def get_AccessToken(req:GetAccessTokenReq)->GetAccessTokenResp:
    url = 'https://oapi.dingtalk.com/gettoken'
    params = {
        'appkey': req.appKey,
        'appsecret': req.appSecret
    }
    res = dingtalkRespHandle(requests.get(url, params=params))
    accesstoken = ''
    expires_in = '0'
    if isinstance(res,PlatformResp):
        return GetAccessTokenResp(accesstoken, expires_in,res.getErrCode(),res.getErrMsg())
    if 'access_token' in res:
        accesstoken = res['access_token']
    if 'expires_in' in res:
        expires_in = res['expires_in']
    return GetAccessTokenResp(accesstoken, expires_in)

class SendOtoMessageReq:
    def __init__(self, access_token:str, robotCode:int, userIds:list, msgKey:str,msgParam:any):
        self.access_token = access_token
        self.robotCode = robotCode
        self.userIds = userIds
        self.msgKey = msgKey
        self.msgParam = msgParam

class SendOtoMessageResp(PlatformResp):
    def __init__(self, processQueryKey:str=None,invalidStaffIdList:list=None,flowControlledStaffIdList:list=None,errcode='0',errmsg='ok'):
        super().__init__(errcode,errmsg)
        self.processQueryKey = processQueryKey
        self.invalidStaffIdList = invalidStaffIdList
        self.flowControlledStaffIdList = flowControlledStaffIdList

    def get_process_query_key(self):
        return self.processQueryKey
    
    def get_invalid_staff_id_list(self):
        return self.invalidStaffIdList
    
    def get_flow_controlled_staff_id_list(self):
        return self.flowControlledStaffIdList
    
    def __str__(self):
        return f"SendOtoMessageResp(processQueryKey={self.processQueryKey}, invalidStaffIdList={self.invalidStaffIdList}, flowControlledStaffIdList={self.flowControlledStaffIdList}, errcode={self.errcode}, errmsg={self.errmsg})"

def send_otoMessage(req:SendOtoMessageReq)->SendOtoMessageResp:
    #创建机器人批量发送单聊请求
    url = 'https://api.dingtalk.com/v1.0/robot/oToMessages/batchSend'
    params = {
        'x-acs-dingtalk-access-token': req.access_token,#必填
    }
    body = {
        "msgKey": req.msgKey, #消息类型，可指定模板
        "msgParam": req.msgParam,
        "robotCode": req.robotCode, #机器人ID
        "userIds": req.userIds
    }
    resp = dingtalkRespHandle(requests.post(url,params=params,json=body))
    processQueryKey = ''
    invalidStaffIdList = flowControlledStaffIdList = []
    if isinstance(resp,PlatformResp):
        return SendOtoMessageResp(processQueryKey,invalidStaffIdList,flowControlledStaffIdList,resp.getErrCode(),resp.getErrMsg())
    if 'processQueryKey' in resp:
        processQueryKey = resp['processQueryKey']
    if 'invalidStaffIdList' in resp:
        invalidStaffIdList = resp['invalidStaffIdList']
    if 'flowControlledStaffIdList' in resp:
        flowControlledStaffIdList = resp['flowControlledStaffIdList']
    return SendOtoMessageResp(processQueryKey, invalidStaffIdList, flowControlledStaffIdList)

def send_groupMessage(req:SendWebhookMessageReq):
    resp = dingtalkRespHandle(send_WebhookMessage(req))
    if isinstance(resp,PlatformResp):
        return resp
    return PlatformResp()

