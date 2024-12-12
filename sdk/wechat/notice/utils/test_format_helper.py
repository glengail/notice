from sdk.wechat.notice.utils.format_helper import *
def test_list2FormattedIds():
    userlist1 = ['user1','user2','user3']
    userlist2 = []
    userlist3 = ['user1']
    assert list2FormattedIds(userlist1)=='user1|user2|user3'
    assert list2FormattedIds(userlist2)==''
    assert list2FormattedIds(userlist3)=='user1'

def test_formattedIds2List():
    formattedIds1 = 'user1|user2|user3'
    formattedIds2 = ''
    formattedIds3 = 'user1'
    assert formattedIds2List(formattedIds1)==['user1','user2','user3']
    assert formattedIds2List(formattedIds2)==[]
    assert formattedIds2List(formattedIds3)==['user1']

