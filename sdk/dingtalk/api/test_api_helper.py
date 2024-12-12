import requests
import requests_mock
from sdk._platform.api.api_helper import PlatformResp, GetAccessTokenResp
from sdk.dingtalk.api.api_helper import *
# 这里的your_module_name需要替换为实际包含上述代码的模块名，如果代码就在当前测试文件同目录下的.py文件中，可以直接写文件名（不含.py后缀）

# 测试dingtalkRespHandle函数
def test_dingtalkRespHandle():
    """测试dingtalkRespHandle函数"""
    # 模拟成功的响应（状态码为200且无错误码）
    with requests_mock.Mocker() as m:
        m.get('https://example.com', status_code=200, json={})
        response = requests.get('https://example.com')
        result = dingtalkRespHandle(response)
        assert not isinstance(result,PlatformResp)

    # 模拟状态码不为200的响应
    with requests_mock.Mocker() as m:
        m.get('https://example.com', status_code=404,reason='page not found')
        response = requests.get('https://example.com')
        result = dingtalkRespHandle(response)
        assert isinstance(result,PlatformResp)
        assert result.getErrCode() == '404'
        assert result.getErrMsg() == 'page not found'

    # 模拟包含错误码的响应
    with requests_mock.Mocker() as m:
        m.get('https://example.com', status_code=200, json={'code': 1, 'message': 'error'})
        response = requests.get('https://example.com')
        result = dingtalkRespHandle(response)
        assert isinstance(result,PlatformResp)
        assert result.getErrCode() == '1'
        assert result.getErrMsg() == 'error'

# 测试get_AccessToken函数
def test_get_AccessToken():

    req = GetAccessTokenReq(
        'dingg8zsyvwmdian9bp6',
        '3Y_CV5ANbiJZji1idDMxYOufLTMFkeEIiI63PUTkWC5rN77hNY5XAwRQ0pgCZS7r'
    )
    # 模拟成功获取访问令牌的情况
    with requests_mock.Mocker() as m:
        m.get('https://oapi.dingtalk.com/gettoken', status_code=200,
              json={'access_token': 'test_token', 'expires_in': '1800'})
        result = get_AccessToken(req)
        assert isinstance(result, GetAccessTokenResp)
        assert result.getAccessToken() == 'test_token'
        assert result.getExpires_in() == '1800'

    # 模拟获取访问令牌失败（比如返回非200状态码）的情况
    with requests_mock.Mocker() as m:
        m.get('https://oapi.dingtalk.com/gettoken', status_code=404,reason='Not Found')
        result = get_AccessToken(req)
        assert isinstance(result,GetAccessTokenResp)
        assert result.getErrCode() == '404'
        assert result.getErrMsg() == 'Not Found'
        assert result.getAccessToken() == ''
        assert result.getExpires_in() == '0'

    # 无效凭证
    with requests_mock.Mocker() as m:
        m.get('https://oapi.dingtalk.com/gettoken', status_code=200, json={'code': 'invalidClientIdOrSecret', 'message': '无效的clientId或者clientSecret'})
        result = get_AccessToken(req)
        assert isinstance(result, GetAccessTokenResp)
        assert result.getErrCode() == 'invalidClientIdOrSecret'
        assert result.getErrMsg() == '无效的clientId或者clientSecret'
        assert result.getAccessToken() == ''
        assert result.getExpires_in() == '0'

# 测试send_otoMessage函数
def test_send_otoMessage():
    req = SendOtoMessageReq('test_access_token', 123, ['user1', 'user2'], 'test_msgKey', {'param': 'value'})
    # 模拟发送消息成功的情况
    with requests_mock.Mocker() as m:
        m.post('https://api.dingtalk.com/v1.0/robot/oToMessages/batchSend', status_code=200,json={'processQueryKey': 'test_key', 'invalidStaffIdList': [],'flowControlledStaffIdList': []})
        result = send_otoMessage(req)
        assert isinstance(result, SendOtoMessageResp)
        assert result.processQueryKey == 'test_key'
        assert result.invalidStaffIdList == []
        assert result.flowControlledStaffIdList == []

    # 模拟发送消息失败（比如返回非200状态码）的情况
    with requests_mock.Mocker() as m:
        m.post('https://api.dingtalk.com/v1.0/robot/oToMessages/batchSend', status_code=404,reason='Not Found')
        result = send_otoMessage(req)
        assert isinstance(result, SendOtoMessageResp)
        assert result.getErrCode() == '404'
        assert result.getErrMsg() == 'Not Found'

    # 无效内容类型
    with requests_mock.Mocker() as m:
        m.post('https://api.dingtalk.com/v1.0/robot/oToMessages/batchSend', status_code=200, json={'code': 'invalidParameter.msgKey.invalid', 'message': 'description: 不支持类型 sampleMarkdow ;solution:请使用支持的类型;link:请参考本接口对应文档查看支持的消息类型，或者在https://open.dingtalk.com/document/ 搜索对应文档;'})
        result = send_otoMessage(req)
        assert isinstance(result, SendOtoMessageResp)
        assert result.getErrCode() == 'invalidParameter.msgKey.invalid'
        assert result.getErrMsg() == 'description: 不支持类型 sampleMarkdow ;solution:请使用支持的类型;link:请参考本接口对应文档查看支持的消息类型，或者在https://open.dingtalk.com/document/ 搜索对应文档;'

def test_send_groupMessage():
    req = SendWebhookMessageReq(
        url='https://oapi.dingtalk.com/robot/send?access_token=XXXXXX',
        content = {'text':'test'}
    )
     # 模拟发送消息成功的情况
    with requests_mock.Mocker() as m:
        m.post('https://oapi.dingtalk.com/robot/send', status_code=200,json={'errcode':0,'errmsg':'ok'})
        result = send_groupMessage(req)
        assert result.getErrCode() == '0'
        assert result.getErrMsg() =='ok'
    # 模拟发送消息失败（比如返回非200状态码）的情况
    with requests_mock.Mocker() as m:
        m.post('https://oapi.dingtalk.com/robot/send', status_code=404,reason='Not Found',)
        result = send_groupMessage(req)
        assert isinstance(result, PlatformResp)
        assert result.getErrCode() == '404'
        assert result.getErrMsg() == 'Not Found'

    # 无效内容类型
    with requests_mock.Mocker() as m:
        m.post('https://oapi.dingtalk.com/robot/send', status_code=200, json={'errcode': 4002, 'errmsg': 'description:参数 text --》 content 缺失，或者参数格式不正确; solution:请填充上对应参数;link:请参考本接口对应文档查看参数获取方式，或者在https://open.dingtalk.com/document/  搜索对应文档;'})
        result = send_groupMessage(req)
        assert result.getErrCode() == '4002'
        assert result.getErrMsg() == 'description:参数 text --》 content 缺失，或者参数格式不正确; solution:请填充上对应参数;link:请参考本接口对应文档查看参数获取方式，或者在https://open.dingtalk.com/document/  搜索对应文档;'
