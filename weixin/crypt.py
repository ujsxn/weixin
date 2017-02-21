# coding: utf8
import hashlib


def validate(token, timestamp, nonce, signature):
    """
    验证服务器地址有效性

    :param token: Token可由开发者可以任意填写，用作生成签名（该Token会和接口URL中包含的Token进行比对，从而验证安全性）
    :param timestamp: 时间戳
    :param nonce: 随机数
    :param signature: 微信加密签名，signature结合了开发者填写的token参数和请求中的timestamp参数、nonce参数。
    :return:
    """
    try:
        # 将token、timestamp、nonce三个参数进行字典序排序
        raw_list = [token, timestamp, nonce]
        raw_list.sort()

        # 将三个参数字符串拼接成一个字符串进行sha1加密
        sha = hashlib.sha1()
        sha.update("".join(raw_list))

        # 开发者获得加密后的字符串可与signature对比，标识该请求来源于微信
        if signature == sha.hexdigest():
            return True
    except Exception:
        return False

