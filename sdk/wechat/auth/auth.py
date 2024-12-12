from sdk._platform.auth.auth import Authentication
from sdk.wechat.api.api_helper import get_AccessToken,GetAccessTokenReq
class WechatAuthentication(Authentication):
    class TokenCache(Authentication.TokenCache):
        def update_token(self):
            resp = get_AccessToken(GetAccessTokenReq(self.auth.getKey(),self.auth.getSecret()))
            super().set_token(resp.getAccessToken(),float(resp.getExpires_in()))

    def setCorpId(self,corpId:str):
        super().setKey(corpId)
        return self

    def getCorpId(self):
        return super().getKey()
    
    def setCorpSecret(self,corpSecret:str):
        super().setSecret(corpSecret)
        return self

    def getCorpSecret(self):
        return super().getSecret()
