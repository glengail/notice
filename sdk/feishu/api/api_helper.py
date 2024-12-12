import requests
from sdk._platform.api.api_helper import *
def feishuRespHandle(resp:requests.models.Response):
    if resp.status_code != 200:
        return PlatformResp(str(resp.status_code),resp.reason)
    errcode = resp.json()['code']
    if errcode !=0 and errcode != '0':
        if 'msg' in resp.json():
            errmsg = resp.json()['msg']
        return PlatformResp(str(errcode),str(errmsg))
    return resp.json()

class GetAccessTokenReq:
    def __init__(self, appID:str, appSecret:str):
        self.appID= appID
        self.appSecret = appSecret

    def getAppID(self):
        return self.appID
    
    def getAppSecret(self):
        return self.appSecret
    
def get_AccessToken(req:GetAccessTokenReq):
    url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
    body = {
        'app_id': req.getAppID(),
        'app_secret': req.getAppSecret()
    }
    res = feishuRespHandle(requests.post(url, json=body))
    if isinstance(res,PlatformResp):
        return GetAccessTokenResp('','0',res.getErrCode(),res.getErrMsg())
    return GetAccessTokenResp(res['tenant_access_token'],res['expire'])

class SendOtoMessageReq:
    def __init__(self, accessToken:str, msgType:str, content:any, department_ids:list, open_ids:list, user_ids:list,union_ids:list,card:any=None):
        self.accessToken = accessToken
        self.msgType = msgType
        self.content = content
        self.department_ids = department_ids
        self.open_ids = open_ids
        self.user_ids = user_ids
        self.union_ids = union_ids
        self.card = card

class SendOtoMessageResp(PlatformResp):
    def __init__(self,invalid_department_ids=[],invalid_open_ids=[],invalid_user_ids=[],invalid_union_ids=[],errcode='0',errmsg='ok'):
        super().__init__(errcode,errmsg)
        self.invalid_department_ids = invalid_department_ids
        self.invalid_open_ids = invalid_open_ids
        self.invalid_user_ids = invalid_user_ids
        self.invalid_union_ids = invalid_union_ids

    def get_invalid_department_ids(self)->list:
        return self.invalid_department_ids
    
    def get_invalid_open_ids(self)->list:
        return self.invalid_open_ids
    
    def get_invalid_user_ids(self)->list:
        return self.invalid_user_ids
    
    def get_invalid_union_ids(self)->list:
        return self.invalid_union_ids
    
    def __str__(self):
        return f"SendOtoMessageResp(invalid_department_ids={self.invalid_department_ids}, invalid_open_ids={self.invalid_open_ids}, invalid_user_ids={self.invalid_user_ids}, invalid_union_ids={self.invalid_union_ids}, errcode='{self.errcode}', errmsg='{self.errmsg}')"

def sendOtoMessage(req:SendOtoMessageReq)->SendOtoMessageResp:
    url = 'https://open.feishu.cn/open-apis/message/v4/batch_send'
    headers = {
        'Authorization':f'Bearer {req.accessToken}',
        'Content-Type':'application/json'
    }
    payload = {
        'content': req.content,
        'msg_type': req.msgType,
    }
    if req.department_ids is not None:
        payload['department_ids'] = req.department_ids
    if req.open_ids is not None:
        payload['open_ids'] = req.open_ids
    if req.user_ids is not None:
        payload['user_ids'] = req.user_ids
    if req.union_ids is not None:
        payload['union_ids'] = req.union_ids
    if req.card is not None:
        payload['card'] = req.card
    res = feishuRespHandle(requests.post(url, headers=headers, json=payload))
    if isinstance(res,PlatformResp):
        return SendOtoMessageResp(errcode=res.getErrCode(),errmsg=res.getErrMsg())
    if 'data' in res:
            res = res['data']
            invalid_department_ids = invalid_open_ids = invalid_user_ids = invalid_union_ids = []
            if 'invalid_department_ids' in res:
                invalid_department_ids = res['invalid_department_ids']
            if 'invalid_open_ids' in res:
                invalid_open_ids = res['invalid_open_ids']
            if 'invalid_user_ids' in res:
                invalid_user_ids = res['invalid_user_ids']
            if 'invalid_union_ids' in res:
                invalid_union_ids = res['invalid_union_ids']
            return SendOtoMessageResp(
                invalid_department_ids,
                invalid_open_ids,
                invalid_user_ids,
                invalid_union_ids
                )
    return SendOtoMessageResp(errcode='error',errmsg='未知错误')

def send_groupMessage(req:SendWebhookMessageReq):
    resp = feishuRespHandle(send_WebhookMessage(req))
    if isinstance(resp,PlatformResp):
        return resp
    return PlatformResp()
