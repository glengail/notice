from sdk._platform.notice.receivers import Receivers as _Receivers
from sdk.feishu.notice.message import *
class Receivers(_Receivers):
    def __init__(self):
        super().__init__()
        self.departmentIds = []
        self.openIds = []
        self.unionIds = []

    def add_unionId(self,unionId):
        self.unionIds.append(unionId)
        return self
    
    def set_unionIds(self,unionIds:list):
        self.unionIds = unionIds
        return self.get_unionIds()

    def add_department(self, departmentId):
        self.departmentIds.append(departmentId)
        return self
    
    def set_departmentIds(self, departmentIds:list):
        self.departmentIds = departmentIds
        return self.get_departmentIds()
    
    def add_openId(self, openId):
        self.openIds.append(openId)
        return self
    
    def set_openIds(self, openIds:list):
        self.openIds = openIds
        return self.get_openIds()
    
    def get_unionIds(self)->list:
        if self.unionIds is None:
            self.unionIds = []
        return self.unionIds

    def get_departmentIds(self)->list:
        if self.departmentIds is None:
            self.departmentIds = []
        return self.departmentIds
    
    def get_openIds(self)->list:
        if self.openIds is None:
            self.openIds = []
        return self.openIds
    
    def hasReceivers(self)->bool:
        return super().hasReceivers() or not (self.departmentIds == self.openIds == self.unionIds == None or len(self.unionIds) == len(self.departmentIds) == len(self.openIds) == 0)
    
    

        