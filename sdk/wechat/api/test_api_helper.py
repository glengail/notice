import requests
import requests_mock
from sdk._platform.api.api_helper import GetAccessTokenResp, PlatformResp
from sdk.wechat.api.api_helper import *

# 测试wechatRespHandle函数
def test_wechatRespHandle():
    """测试wechatRespHandle函数"""
    # 模拟状态码不为200的响应
    with requests_mock.Mocker() as m:
        m.get('https://example.com', status_code=404,reason = 'Not Found')
        response = requests.get('https://example.com')
        result = wechatRespHandle(response)
        assert isinstance(result, PlatformResp)
        assert result.getErrCode() == '404'
        assert result.getErrMsg() == "Not Found"

    # 模拟状态码为200但errcode不为0的响应
    with requests_mock.Mocker() as m:
        m.get('https://example.com', status_code=200, json={'errcode': 1, 'errmsg': 'error'})
        response = requests.get('https://example.com')
        result = wechatRespHandle(response)
        assert isinstance(result, PlatformResp)
        assert result.getErrCode() == '1'
        assert result.getErrMsg() == 'error'

    # 模拟状态码为200且errcode为0的响应
    with requests_mock.Mocker() as m:
        m.get('https://example.com', status_code=200, json={'errcode': 0, 'errmsg': 'ok', 'data': 'value'})
        response = requests.get('https://example.com')
        result = wechatRespHandle(response)
        assert result == {'errcode': 0, 'errmsg': 'ok', 'data': 'value'}

# 测试get_AccessToken函数
def test_get_AccessToken():
    req = GetAccessTokenReq('test_corpid', 'test_corpsecret')
    # 模拟成功获取访问令牌的情况
    with requests_mock.Mocker() as m:
        m.get('https://qyapi.weixin.qq.com/cgi-bin/gettoken', status_code=200,
              json={'errcode':0,'errmsg':'ok','access_token': 'test_token', 'expires_in': '1000'})
        result = get_AccessToken(req)
        assert isinstance(result, GetAccessTokenResp)
        assert result.getAccessToken() == 'test_token'
        assert result.getExpires_in() == '1000'

    # 模拟获取访问令牌失败（比如返回非200状态码）的情况
    with requests_mock.Mocker() as m:
        m.get('https://qyapi.weixin.qq.com/cgi-bin/gettoken', status_code=404)
        result = get_AccessToken(req)
        assert isinstance(result, GetAccessTokenResp)
        assert result.getAccessToken() == ''
        assert result.getExpires_in() == '0'

    # 模拟获取访问令牌时返回状态码200但业务errcode不为0的情况
    with requests_mock.Mocker() as m:
        m.get('https://qyapi.weixin.qq.com/cgi-bin/gettoken', status_code=200,
              json={'errcode': 1, 'errmsg': 'error'})
        result = get_AccessToken(req)
        assert isinstance(result, GetAccessTokenResp)
        assert result.getAccessToken() == ''
        assert result.getExpires_in() == '0'

# 测试send_OtoMessage函数
def test_send_OtoMessage():
    req = SendOtoMessageReq('test_access_token', 'test_agentid', 'test_touser', 'test_toparty', 'test_totag',
                            'text', 'test_content', '0', '0', '0', '1800')
    # 模拟发送消息成功的情况
    with requests_mock.Mocker() as m:
        m.post('https://qyapi.weixin.qq.com/cgi-bin/message/send', status_code=200,
               json={'errcode': 0, 'errmsg': 'ok', 'invaliduser': '', 'invalidparty': '', 'invalidtag': ''})
        result = send_OtoMessage(req)
        assert isinstance(result, SendOtoMessageResp)
        assert result.getErrCode() == '0'
        assert result.getErrMsg() == 'ok'
        assert result.getInvalidUser() == ''
        assert result.getInvalidParty() == ''
        assert result.getInvalidTag() == ''

    # 模拟发送消息失败（比如返回非200状态码）的情况
    with requests_mock.Mocker() as m:
        m.post('https://qyapi.weixin.qq.com/cgi-bin/message/send', status_code=404,reason='Not Found')
        result = send_OtoMessage(req)
        assert isinstance(result, SendOtoMessageResp)
        assert result.getErrCode() == '404'
        assert result.getErrMsg() == "Not Found"
        assert result.getInvalidUser() == ''
        assert result.getInvalidParty() == ''
        assert result.getInvalidTag() == ''

    # 模拟发送消息时返回状态码200但业务errcode不为0的情况
    with requests_mock.Mocker() as m:
        m.post('https://qyapi.weixin.qq.com/cgi-bin/message/send', status_code=200,
               json={'errcode': 1, 'errmsg': 'error', 'invaliduser': '', 'invalidparty': '', 'invalidtag': ''})
        result = send_OtoMessage(req)
        assert isinstance(result, SendOtoMessageResp)
        assert result.getErrCode() == '1'
        assert result.getErrMsg() == 'error'
        assert result.getInvalidUser() == ''
        assert result.getInvalidParty() == ''
        assert result.getInvalidTag() == ''

    # 有部分无效user
    with requests_mock.Mocker() as m:
        m.post('https://qyapi.weixin.qq.com/cgi-bin/message/send', status_code=200,
               json={'errcode': 0, 'errmsg': 'ok', 'invaliduser': 'test_invalid_user|test_invalid_user2', 'invalidparty': '', 'invalidtag': ''})
        result = send_OtoMessage(req)
        assert isinstance(result, SendOtoMessageResp)
        assert result.getErrCode() == '0'
        assert result.getErrMsg() == 'ok'
        assert result.getInvalidUser() == 'test_invalid_user|test_invalid_user2'
        assert result.getInvalidParty() == ''
        assert result.getInvalidTag() == ''

def test_send_groupMessage():
    req = SendWebhookMessageReq(
        url='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=23f49e25-98ca-40d7-af48-d78a262729c7',
        content = {'text':'test'}
    )
     # 模拟发送消息成功的情况
    with requests_mock.Mocker() as m:
        m.post('https://qyapi.weixin.qq.com/cgi-bin/webhook/send', status_code=200,json={'errcode':0,'errmsg':'ok'})
        result = send_groupMessage(req)
        assert result.getErrCode() == '0'
        assert result.getErrMsg() =='ok'
    # 模拟发送消息失败（比如返回非200状态码）的情况
    with requests_mock.Mocker() as m:
        m.post('https://qyapi.weixin.qq.com/cgi-bin/webhook/send', status_code=404,reason='Not Found',)
        result = send_groupMessage(req)
        assert isinstance(result, PlatformResp)
        assert result.getErrCode() == '404'
        assert result.getErrMsg() == 'Not Found'

    # 无效内容类型
    with requests_mock.Mocker() as m:
        m.post('https://qyapi.weixin.qq.com/cgi-bin/webhook/send', status_code=200, json={'errcode': 4002, 'errmsg': 'error'})
        result = send_groupMessage(req)
        assert result.getErrCode() == '4002'
        assert result.getErrMsg() == 'error'
