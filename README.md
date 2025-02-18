# notice
第三方通知(钉钉、企业微信、飞书)
使用说明：

运行容器暴露5000端口(默认，在notice.toml)，post访问地址0.0.0.0:5000/notice/platform

请求参数为json

platform：平台，传dingtalk/wechat/feishu

receivers：消息接收者的userid(list)，用于通知到个人

content：消息内容，文本/json格式(通知到飞书的webhook即使用“数据推送机器人”，消息内容需改成json)

key：钉钉传appkey，企业微信传corpid，飞书传appid

secret：钉钉传appsecret，企业微信传corpsecret，飞书传appsecret

agentid: 应用id，仅单聊通知企业微信需要传

webhook_urls：用于企业微信、钉钉通知到群聊，飞书的“数据推送”机器人

例子1：通知飞书

{

​    "platform":"feishu",

​    "receivers":["user1"],

​    "content": "测试RPA\n这是第二行",

​    "key":"XXXXXXXXX",

​    "secret":"XXXXXXXXXXXXXX"

}

例子2：通知飞书(使用webhook数据推送机器人)

{

​    "platform":"feishu",

​    "content": {"text":"测试RPA\n这是第二行"},

​    "webhook_urls":["https://www.feishu.cn/flow/api/trigger-webhook/XXXXXXXXXXXXXXXXXXXXX"]

}

例子3：通知企业微信(同时通知到个人和群聊)

{

​    "platform":"wechat",

​    "receivers":["user1","user2"],

​    "content": "测试RPA\n这是第二行",

​    "key":"XXXXXXXXX",

​    "secret":"XXXXXXXXX",

​	“agentid":"10002",

​    "webhook_urls":["https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=123,"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=1234"]

}

例子4：通知钉钉(同时通知到个人和群聊)

{

​    "platform":"dingtalk",

​    "receivers":["user1"],

​    "content": "测试RPA\n这是第二行",

​    "key":"XXXXXXXXX",

​    "secret":"XXXXXXXXX",

​    "webhook_urls":["https://oapi.dingtalk.com/robot/send?access_token=123","https://oapi.dingtalk.com/robot/send?access_token=1234"]

}



