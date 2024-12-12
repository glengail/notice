from sdk._platform.notice.receivers import Receivers as _Receivers
from sdk.wechat.notice.utils.format_helper import list2FormattedIds
class Receivers(_Receivers):
    def __init__(self):
        super().__init__()
        self.departmentIds = []
        self.tagIds = []

    def add_department(self, departmentId):
        self.departmentIds.append(departmentId)
        return self

    def add_tag(self, tagId):
        self.tagIds.append(tagId)
        return self

    def set_departmentIds(self, departmentIds:list):
        self.departmentIds = departmentIds
        return self

    def get_departmentIds(self)->list:
        if self.departmentIds is None:
            self.departmentIds = []
        return self.departmentIds

    def set_tagIds(self, tagIds:list)->list:
        self.tagIds = tagIds
        return self

    def get_tagIds(self)->list:
        if self.tagIds is None:
            self.tagIds = []
        return self.tagIds

    def get_formatedUserIds(self):
        return list2FormattedIds(self.get_userIds())
    
    def get_formatedDepartmentIds(self):
        return list2FormattedIds(self.get_departmentIds())
    
    def add_allUsers(self):
        super().get_userIds().clear()
        super().add_user('@all')

    def add_allDepartments(self):
        self.get_departmentIds().clear()
        self.add_department('@all')

    def add_allTags(self):
        self.get_tagIds().clear()
        self.add_tag('@all')
        

    def hasReceivers(self)->bool:
        return super().hasReceivers() or not (self.departmentIds == self.tagIds == None or len(self.departmentIds) == len(self.tagIds) == 0)
    
    def get_formatedTagIds(self):
        return list2FormattedIds(self.get_tagIds())