import requests
import requests_mock
from sdk._platform.api.api_helper import *
from sdk.feishu.api.api_helper import *

# 测试FeishuRespHandle函数
def test_feishuRespHandle():
    """测试FeishuRespHandle函数"""
    # 模拟成功的响应（状态码为200且无错误码）
    with requests_mock.Mocker() as m:
        m.post('https://example.com', status_code=200, json={'code': 0, 'msg': 'ok'})
        response = requests.post('https://example.com')
        result = feishuRespHandle(response)
        assert not isinstance(result, PlatformResp)

    # 模拟状态码不为200的响应
    with requests_mock.Mocker() as m:
        m.post('https://example.com', status_code=404,reason='Not Found')
        response = requests.post('https://example.com')
        result = feishuRespHandle(response)
        assert isinstance(result,PlatformResp)
        assert result.getErrCode() == '404'
        assert result.getErrMsg() == 'Not Found'

    # 模拟包含错误码（errcode不为0）的响应
    with requests_mock.Mocker() as m:
        m.post('https://example.com', status_code=200, json={'code': 1, 'msg': 'error'})
        response = requests.post('https://example.com')
        result = feishuRespHandle(response)
        assert isinstance(result,PlatformResp)
        assert result.getErrCode() == '1'
        assert result.getErrMsg() == 'error'

# 测试get_AccessToken函数
def test_get_AccessToken():
    req = GetAccessTokenReq('test_appID', 'test_appSecret')
    # 模拟成功获取访问令牌的情况
    with requests_mock.Mocker() as m:
        m.post('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', status_code=200,
               json={'code':0,'msg':'ok','tenant_access_token': 'test_token', 'expire': '1000'})
        result = get_AccessToken(req)
        assert isinstance(result, GetAccessTokenResp)
        assert result.getAccessToken() == 'test_token'
        assert result.getExpires_in() == '1000'

    # 模拟获取访问令牌失败（比如返回非200状态码）的情况
    with requests_mock.Mocker() as m:
        m.post('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', status_code=404,reason='Not Found')
        result = get_AccessToken(req)
        assert isinstance(result, GetAccessTokenResp)
        assert result.getErrCode() == '404'
        assert result.getErrMsg() == 'Not Found'
        assert result.getAccessToken() == ''
        assert result.getExpires_in() == '0'

    # 无效凭证
    with requests_mock.Mocker() as m:
        m.post('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', status_code=200,json={'code':1,'msg':'invalid_credentials'})
        result = get_AccessToken(req)
        assert isinstance(result, GetAccessTokenResp)
        assert result.getErrCode() == '1'
        assert result.getErrMsg() == 'invalid_credentials'
        assert result.getAccessToken() == ''
        assert result.getExpires_in() == '0'

# 测试sendOtoMessage函数
def test_sendOtoMessage():
    req = SendOtoMessageReq('test_accessToken', 'text', {'text':'hello'}, ['dep1'], ['open1'], ['user1'], ['union1'])
    # 模拟发送消息成功的情况
    with requests_mock.Mocker() as m:
        m.post('https://open.feishu.cn/open-apis/message/v4/batch_send', status_code=200,
               json={'code':0,'msg':'ok','data': {'invalid_department_ids': [], 'invalid_open_ids': [], 'invalid_user_ids': [],
                              'invalid_union_ids': []}})
        result = sendOtoMessage(req)
        assert isinstance(result, SendOtoMessageResp)
        assert result.getErrCode() == '0'
        assert result.getErrMsg() == 'ok'

    # 模拟发送消息失败（比如返回非200状态码）的情况
    with requests_mock.Mocker() as m:
        m.post('https://open.feishu.cn/open-apis/message/v4/batch_send', status_code=404,reason='Not Found')
        result = sendOtoMessage(req)
        assert isinstance(result, SendOtoMessageResp)
        assert result.getErrCode() == '404'
        assert result.getErrMsg() == 'Not Found'

    # 内容格式非法
    with requests_mock.Mocker() as m:
        m.post('https://open.feishu.cn/open-apis/message/v4/batch_send', status_code=200,
               json={'code':100,'msg':'text require'})
        req.content = {"tet":"你好"}
        result = sendOtoMessage(req)
        assert isinstance(result, SendOtoMessageResp)
        assert result.getErrCode() == '100'
        assert result.getErrMsg() == 'text require'

    #有部分无效用户
    with requests_mock.Mocker() as m:
        m.post('https://open.feishu.cn/open-apis/message/v4/batch_send', status_code=200,
               json={'code':0,'msg':'ok','data':{'invalid_user_ids':["abc"]}})
        req.user_ids = ["abc"]
        result = sendOtoMessage(req)
        assert isinstance(result, SendOtoMessageResp)
        assert result.getErrCode() == '0'
        assert result.getErrMsg() == 'ok'
        assert result.get_invalid_user_ids() == ['abc']

def test_send_groupMessage():
    req = SendWebhookMessageReq(
        url='https://www.feishu.cn/flow/api/trigger-webhook/XXXXXXXXXXX',
        content = {'text':'test'}
    )
     # 模拟发送消息成功的情况
    with requests_mock.Mocker() as m:
        m.post('https://www.feishu.cn/flow/api/trigger-webhook/XXXXXXXXXXX', status_code=200,json={'code':0,'msg':'ok'})
        result = send_groupMessage(req)
        assert result.getErrCode() == '0'
        assert result.getErrMsg() =='ok'
    # 模拟发送消息失败（比如返回非200状态码）的情况
    with requests_mock.Mocker() as m:
        m.post('https://www.feishu.cn/flow/api/trigger-webhook/XXXXXXXXXXX', status_code=404,reason='Not Found',)
        result = send_groupMessage(req)
        assert isinstance(result, PlatformResp)
        assert result.getErrCode() == '404'
        assert result.getErrMsg() == 'Not Found'

    # 无效内容类型
    with requests_mock.Mocker() as m:
        m.post('https://www.feishu.cn/flow/api/trigger-webhook/XXXXXXXXXXX', status_code=200, json={'code': 4002, 'msg': 'error'})
        result = send_groupMessage(req)
        assert result.getErrCode() == '4002'
        assert result.getErrMsg() == 'error'