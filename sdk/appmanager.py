from typing import Union
from sdk.wechat.app import Wechat
from sdk.dingtalk.app import Dingtalk
from sdk.feishu.app import Feishu
from sdk._platform.app import Application

class ApplicationManager:
    @staticmethod
    def create_application(app_type: str)->Application:
        platforms = {
            'wechat':Wechat,
            'dingtalk': Dingtalk,
            'feishu': Feishu 
        }
        return platforms[app_type]()







