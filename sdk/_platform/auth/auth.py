from abc import ABC, abstractmethod
import time
#平台用户凭证的管理类
class Authentication:
    # 令牌缓存的抽象类
    class TokenCache(ABC):
        def __init__(self,auth):
            self.token = None
            self.expiration_time = 0  # 初始化为0，表示当前没有有效的token，时间戳格式
            self.expires_in = 0
            self.auth = auth

        def get_token(self):
            if self._is_token_expired() or self.token is None:
                self.update_token()
                self.expiration_time = time.time() + self.expires_in
            return self.token
        
        def set_token(self, token:str,expires_in:float):
            self.token = token
            self.expires_in = expires_in

        def _is_token_expired(self):
            return time.time() > self.expiration_time
        
        #更新token
        @abstractmethod
        def update_token(self):
            pass
    def __init__(self,key,secret):
        self.key = key
        self.secret = secret
        self.tokenCache = self.TokenCache(self)
    def getAccessToken(self)->str:
        return self.tokenCache.get_token()
    
    def setKey(self,key:str):
        self.key = key

    def getKey(self)->str:
        return self.key
    
    def setSecret(self,secret:str):
        self.secret = secret

    def getSecret(self)->str:
        return self.secret