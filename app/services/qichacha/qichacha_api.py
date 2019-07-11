#!/usr/bin/python
# -*-coding:utf-8-*-
import hashlib
import json
import os
import time

import requests

from app import api

appkey = os.environ['QICHACHA_APPKEY']
seckey = os.environ['QICHACHA_SECRET']
encode = 'utf-8'


def fuzzy_search(keyword):

    # Http请求头设置
    timespan = str(int(time.time()))
    token = appkey + timespan + seckey
    hl = hashlib.md5()
    hl.update(token.encode(encoding=encode))
    token = hl.hexdigest().upper()
    print('MD5加密后为 ：' + token)

    # 设置请求Url-请自行设置Url
    reqInterNme = 'http://api.qichacha.com/ECIV4/Search'
    paramStr = 'keyword=' + keyword
    url = reqInterNme + '?key=' + appkey + '&' + paramStr
    headers = {'Token': token, 'Timespan': timespan}
    response = requests.get(url, headers=headers)

    # 结果返回处理
    print(response.status_code)
    raw_str = response.content.decode()
    print(raw_str)

    result = json.loads(raw_str)
    print(result['Result'])
    return result['Result']


def fuzzy_search_pageIndex(keyword, pageIndex):

    # Http请求头设置
    timespan = str(int(time.time()))
    token = appkey + timespan + seckey
    hl = hashlib.md5()
    hl.update(token.encode(encoding=encode))
    token = hl.hexdigest().upper()
    print('MD5加密后为 ：' + token)

    # 设置请求Url-请自行设置Url
    reqInterNme = 'http://api.qichacha.com/ECIV4/Search'
    paramStr = 'keyword=' + keyword + '&pageIndex=' + str(pageIndex)
    url = reqInterNme + '?key=' + appkey + '&' + paramStr
    headers = {'Token': token, 'Timespan': timespan}
    response = requests.get(url, headers=headers)

    # 结果返回处理
    print(response.status_code)
    raw_str = response.content.decode()
    print(raw_str)

    result = json.loads(raw_str)

    if result['Status'] != '200':
        api.abort(
            500,
            "Qichacha doesn't return results correctly. The error code is {}".format(
                result['Status']
            ),
        )
    print(result['Result'])
    return result['Result'], result['Paging']['TotalRecords']


def basic_detail(keyword):

    # Http请求头设置
    timespan = str(int(time.time()))
    token = appkey + timespan + seckey
    hl = hashlib.md5()
    hl.update(token.encode(encoding=encode))
    token = hl.hexdigest().upper()
    print('MD5加密后为 ：' + token)

    # 设置请求Url-请自行设置Url
    reqInterNme = 'http://api.qichacha.com/ECIV4/GetBasicDetailsByName'
    paramStr = 'keyword=' + keyword
    url = reqInterNme + '?key=' + appkey + '&' + paramStr
    headers = {'Token': token, 'Timespan': timespan}
    response = requests.get(url, headers=headers)

    # 结果返回处理
    print(response.status_code)
    raw_str = response.content.decode()
    print(raw_str)

    result = json.loads(raw_str)
    print(result['Result'])
    return result['Result']
