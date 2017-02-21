# coding: utf8


def response_validate(rsp):
    """
    判断微信接口返回是否正常

    :param rsp:
    :return:
    """

    if rsp.status_code != 200:
        return 1, None

    try:
        content = rsp.json()
    except Exception:
        return 2, None

    if 'errcode' in content and content['errcode'] != 0:
        return 3, None

    return 0, content

