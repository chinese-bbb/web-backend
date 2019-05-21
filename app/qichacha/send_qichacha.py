#!/usr/bin/python
#-*-coding:utf-8-*-

import requests
import time
import hashlib
import json


def send_qichacha(keyword):
    #  请求参数
    appkey = "c7b15705d65f4ce8877b09407c49d2b0"
    seckey = "F753614D3E32BB11E592681376329CE8"
    encode = 'utf-8'

    # Http请求头设置
    timespan = str(int(time.time()))
    token = appkey + timespan + seckey;
    hl = hashlib.md5()
    hl.update(token.encode(encoding=encode))
    token = hl.hexdigest().upper();
    print('MD5加密后为 ：' + token)

    # 设置请求Url-请自行设置Url
    reqInterNme = "http://api.qichacha.com/ECIV4/Search"
    paramStr = "keyword=" + keyword
    url = reqInterNme + "?key=" + appkey + "&" + paramStr;
    headers = {'Token': token, 'Timespan': timespan}
    response = requests.get(url, headers=headers)

    # 结果返回处理
    print(response.status_code)
    raw_byte = response.content
    print(raw_byte.decode())

    return raw_byte, str(raw_byte)

