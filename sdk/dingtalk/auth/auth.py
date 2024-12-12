from sdk._platform.auth.auth import Authentication
from sdk.dingtalk.api.api_helper import get_AccessToken,GetAccessTokenReq
class DingtalkAuthentication(Authentication):
    class TokenCache(Authentication.TokenCache):
        def update_token(self):
            resp = get_AccessToken(GetAccessTokenReq(self.auth.getKey(),self.auth.getSecret()))
            super().set_token(resp.getAccessToken(),float(resp.getExpires_in()))
            
    def getAppSecret(self)->str:
        return super().getSecret()
    
    def setAppSecret(self,appSecret:str):
        super().setSecret(appSecret)

    def setAppKey(self,appKey:str):
        super().setKey(appKey)

    def getAppSecret(self):
        return super().getSecret()