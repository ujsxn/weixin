# coding: utf8
import requests
import logging


from utils import response_validate

logger = logging.getLogger("weixin")


class WxBaseApi(object):

    API_URL_PREFIX = 'https://api.weixin.qq.com/cgi-bin/'

    def __init__(self, manager=None):
        self.manager = manager
        self._access_token = None

    @property
    def access_token(self):
        if self._access_token:
            logger.debug("[access_token] customer provided")
            return self._access_token
        else:
            if self.manager:
                return self.manager.get_access_token()
            else:
                logger.error("[access_token] No way to get access_token")
                return None

    @access_token.setter
    def access_token(self, value):
        self._access_token = value

    def _get(self, url, params=None):
        """
        GET

        :param url: 请求的url
        :param params: 需附在get请求的query string中的值 dict类型
        :return:
        """
        if not params:
            params = {}
        params['access_token'] = self.access_token
        rsp = requests.get(self.API_URL_PREFIX + url, params=params)

        logger.debug("[_get] %s" % rsp.content)
        return response_validate(rsp)

    def _post(self, url, data, params=None):
        """
        POST

        :param url: 请求的url
        :param data: 数据
        :return:
        """
        if not params:
            params = {}
        params['access_token'] = self.access_token
        rsp = requests.post(self.API_URL_PREFIX + url, data=data, params=params)

        logger.debug("[_post] %s" % rsp.content)
        return response_validate(rsp)


class WxApiPersonal(WxBaseApi):

    # 基础

    def get_weichat_ip(self):
        """
        获取微信服务器ip地址

        :return:

        {
            "ip_list": [
            "127.0.0.1",
            "127.0.0.2",
            "101.226.103.0/25"
            ]
        }
        """
        return self._get("getcallbackip")


class WxApiPublic(WxApiPersonal):

    # 信息获取

    def user_info(self, user_id, lang='zh_CN'):
        """
        获取用户基本信息（包括UnionID机制）

        :param user_id: 普通用户的标识，对当前公众号唯一
        :param lang: 返回国家地区语言版本，zh_CN 简体，zh_TW 繁体，en 英语
        :return:

            {
                "subscribe": 1,
                "openid": "o6_bmjrPTlm6_2sgVt7hMZOPfL2M",
                "nickname": "Band",
                "sex": 1,
                "language": "zh_CN",
                "city": "广州",
                "province": "广东",
                "country": "中国",
                "headimgurl":    "http://wx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/0",
                "subscribe_time": 1382694957,
                "unionid": " o6_bmasdasdsad6_2sgVt7hMZOPfL"
                "remark": "",
                "groupid": 0
            }
            参数说明:

            subscribe	用户是否订阅该公众号标识，值为0时，代表此用户没有关注该公众号，拉取不到其余信息，只有openid和UnionID（在该公众号绑定到了微信开放平台账号时才有）。
            openid	用户的标识，对当前公众号唯一
            nickname	用户的昵称
            sex	用户的性别，值为1时是男性，值为2时是女性，值为0时是未知
            city	用户所在城市
            country	用户所在国家
            province	用户所在省份
            language	用户的语言，简体中文为zh_CN
            headimgurl	用户头像，最后一个数值代表正方形头像大小（有0、46、64、96、132数值可选，0代表640*640正方形头像），用户没有头像时该项为空。若用户更换头像，原有头像URL将失效。
            subscribe_time	用户关注时间，为时间戳。如果用户曾多次关注，则取最后关注时间
            unionid	只有在用户将公众号绑定到微信开放平台帐号后，才会出现该字段。详见：获取用户个人信息（UnionID机制）
            remark	公众号运营者对粉丝的备注，公众号运营者可在微信公众平台用户管理界面对粉丝添加备注
            groupid	用户所在的分组ID

            {"errcode":40013,"errmsg":"invalid appid"}

        """
        return self._get('user/info', {'openid': user_id, 'lang': lang})

    def user_list(self, next_id):
        """
        获取帐号的关注者列表，关注者列表由一串OpenID（加密后的微信号，每个用户对每个公众号的OpenID是唯一的）组成。
        一次拉取调用最多拉取10000个关注者的OpenID，可以通过多次拉取的方式来满足需求。

        :param next_id: 第一个拉取的OPENID，不填默认从头开始拉取
        :return:

            {"total":2,"count":2,"data":{"openid":["","OPENID1","OPENID2"]},"next_openid":"NEXT_OPENID"}
            {"errcode":40013,"errmsg":"invalid appid"}

        """
        if next_id:
            return self._get('user/get', {'next_openid': next_id})
        return self._get('user/get')

    # 消息发送（客服消息发送）

    def send_text(self, to_user, content):
        """
        发送文本消息

        :param to_user:
        :param content:
        :return:
        """
        data = {
            'touser': to_user,
            'msgtype': 'text',
            'text': {
                'content': content
            }
        }
        return self._post('message/custom/send', data)

    def send_image(self, to_user, media_id=None):
        """
        发送图片消息

        :param to_user:
        :param media_id:
        :param media_url:
        :return:
        """

        data = {
            "touser": to_user,
            "msgtype": "image",
            "image": {
                    "media_id": media_id
            }
        }
        return self._post('message/custom/send', data)

    def send_voice(self, to_user, media_id=None):
        """
        发送语音消息

        :param to_user:
        :return:
        """
        data = {
            "touser": to_user,
            "msgtype": "voice",
            "voice": {
                    "media_id": media_id
            }
        }
        return self._post('message/custom/send', data)

    # 用户分组管理

    def create_group(self, name):
        return self._post('groups/create',
                          {'group': {'name': name}})

    def groups(self):
        return self._get('groups/get')

    def update_group(self, group_id, name):
        return self._post('groups/update',
                          {'group': {'id': group_id, 'name': name}})

    def group_of_user(self, user_id):
        return self._get('groups/getid', {'openid': user_id})

    def move_user_to_group(self, user_id, group_id):
        return self._post('groups/members/update',
                          {'openid': user_id, 'to_groupid': group_id})

    # 自定义菜单管理

    def create_menu(self, menus):
        return self._post('menu/create', menus)

    def get_menu(self):
        return self._get('menu/get')

    def delete_menu(self):
        return self._get('menu/delete')

    # 素材管理


if __name__ == "__main__":

    api = WxApiPersonal()
    api.access_token = "36knMxM6WasfLXi66Q8a-n_G1K02i4gKjlEY5uWVr6ff2t1fVQfeYKTeqxAHjGYnpfhr24Up-CoeZSSUMZI3TZWhTxyeaGUjIH5ljct2JWMFFAcAIAPPK"
    print api.get_weichat_ip()