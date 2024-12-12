#消息通知的接收者
class Receivers:
    def __init__(self):
        self.userIds = []

    def add_user(self, userId:str):
        self.get_userIds().append(userId)
        return self
    
    def get_userIds(self)->list:
        if self.userIds is None:
            self.userIds = []
        return self.userIds
    
    def set_userIds(self, userIds:list)->list:
        self.userIds = userIds
        return self.get_userIds()
    
    def hasReceivers(self)->bool:
        return not (self.userIds is None or len(self.userIds) == 0)