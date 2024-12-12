from sdk._platform.auth.auth import *
import random

class testauth(Authentication):
     class TokenCache(Authentication.TokenCache):
        def update_token(self):
            super().set_token(random.randint(1, 100),float(2))
def test_get_token():
    #测试缓存
    auth = testauth('testkey','testsecret')
    for i in range (2):
        token1 = auth.getAccessToken()
        time.sleep(1)
        token2 = auth.getAccessToken()
        assert token1 == token2
        time.sleep(2)
        token3 = auth.getAccessToken()
        assert token2 != token3
