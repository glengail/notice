import requests

#对接平台api的请求定义
#平台统一响应
class PlatformResp:
    def __init__(self, errcode:str='0',errmsg:str='ok'):
        self.errcode = errcode
        self.errmsg = errmsg
    def getErrCode(self):
        return self.errcode
    def getErrMsg(self):
        return self.errmsg
    
    def __str__(self):
        return f"PlatformResp(errcode={self.getErrCode()}, errmsg={self.getErrMsg()})"

#获取用户平台accessToken请求定义
class GetAccessTokenResp(PlatformResp):
    def __init__(self,token,expired_in,errcode:str='0',errmsg:str='ok'):
        super().__init__(errcode,errmsg)
        self.token = token
        self.expires_in = expired_in
    def getExpires_in(self):
        return self.expires_in
    def getAccessToken(self):
        return self.token
    
class SendWebhookMessageReq:
    def __init__(self,url:str,content:any):
        self.url = url
        self.content = content

#发送各平台webhook消息
def send_WebhookMessage(req:SendWebhookMessageReq):
    url = req.url
    data = req.content
    return requests.post(url,json=data)
