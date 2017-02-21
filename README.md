# 微信API Python sdk

本项目是对微信官方提供的api的封装，方便各种功能的实现，另外提供了access_token的中控器。

## 安装

    pip install weixin

## 使用

    from weixin import Manager, WxApiPublic

    m = Manager(name="1", redis_addr=None, redis_port=6379, redis_password=None, redis_index=1,
                 app_id="xxxxxxxxx", app_secret="xxxxxxx")

    api = WxApiPersonal(m)
    print api.get_weichat_ip()

## Manager

__init__

|名称|类型|描述|起始版本|示例|
|---|---|---|---|---|---|
| name | string |用于该manager的标识|0.1||
| redis_addr |string|redis服务器地址|0.1||
| redis_port |int|redis服务器端口|0.1|0|
| redis_password | string |redis密码|0.1||
| redis_index | int |redis数据库索引|0.1||
| app_id | string |微信公众号的的appid|0.1||
| app_secret | string |微信公众号的appsecret|0.1||

## WxApiPersonal

用于微信公众号个人公众号

    get_weichat_ip 获得微信服务器地址

## WxApiPublic

用于微信公众号订阅号 暂未测试





