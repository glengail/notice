from sdk._platform.auth.auth import Authentication
from sdk.feishu.api.api_helper import get_AccessToken,GetAccessTokenReq
class FeishuAuthentication(Authentication):
    class TokenCache(Authentication.TokenCache):
        def update_token(self):
            resp = get_AccessToken(GetAccessTokenReq(self.auth.getKey(),self.auth.getSecret()))
            super().set_token(resp.getAccessToken(),float(resp.getExpires_in()))

    def setAppId(self,appId:str):
        super().setKey(appId)
        return self
    
    def getAppId(self):
        return super().getKey()
    
    def setAppSecret(self,appSecret:str):
        super().setSecret(appSecret)
        return self
    
    def getAppSecret(self):
        return super().getSecret()
