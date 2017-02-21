# coding: utf8
import requests
import logging
from redis import Redis

from utils import response_validate

logger = logging.getLogger("weixin")


class Manager(object):

    def __init__(self, name="1", redis_addr=None, redis_port=6379, redis_password=None, redis_index=1,
                 app_id="", app_secret=""):

        self.redis_addr = redis_addr
        self.redis_port = redis_port
        self.redis_password = redis_password
        self.redis_index = redis_index
        self.app_id = app_id
        self.app_secret = app_secret
        self.name = name

    def get_access_token(self):
        """
        获得access_token

        :return: access_token
        """
        if self.redis_password:
            redis_cursor = Redis(self.redis_addr, self.redis_port, self.redis_index, self.redis_password)
        else:
            redis_cursor = Redis(self.redis_addr, self.redis_port, self.redis_index)

        r = redis_cursor.get("access_token" + self.name)
        if not r:
            logger.debug("[access_token] Miss")
            flag, access_token = self._token()
            if flag == 0:
                logger.debug("[access_token] Got")
                redis_cursor.set("access_token" + self.name, access_token, ex=7200)
                del redis_cursor
                r = access_token

        logger.info("[access_token] %s" % r)
        return r

    def _token(self):
        """

        获取access token

        grant_type	是	获取access_token填写client_credential
        appid	    是	第三方用户唯一凭证
        secret	    是	第三方用户唯一凭证密钥，即appsecret

        :return:
        """
        params = {
            'grant_type': 'client_credential',
            'appid': self.app_id,
            'secret': self.app_secret
        }

        rsp = requests.get('https://api.weixin.qq.com/cgi-bin/token', params=params)
        logger.info("[_token] " + rsp.content)
        return response_validate(rsp)