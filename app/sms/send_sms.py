#!/usr/bin/python
#-*-coding:utf-8-*-

def send_message(phone):

    appid = 1400205630  # SDK AppID 是1400开头

    # 短信应用 SDK AppKey
    appkey = "b228ae9003292b48327087ab50810cda"

    # 需要发送短信的手机号码
    phone_numbers = [phone]

    # 短信模板 ID，需要在短信应用中申请
    template_id = 324017  # NOTE: 这里的模板 ID`7839`只是一个示例，真实的模板 ID 需要在短信控制台中申请
    # templateId 7839 对应的内容是"您的验证码是: {1}"
    # 签名

    sms_sign = "腾讯云"  # NOTE: 签名参数使用的是`签名内容`，而不是`签名ID`。这里的签名"腾讯云"只是一个示例，真实的签名需要在短信控制台申请。



    from qcloudsms_py import SmsSingleSender
    from qcloudsms_py.httpclient import HTTPError

    ssender = SmsSingleSender(appid, appkey)
    params = ["9273", "5"]  # 当模板没有参数时，`params = []`，数组具体的元素个数和模板中变量个数必须一致，例如示例中 templateId:5678 对应一个变量，参数数组中元素个数也必须是一个
    try:
        result = ssender.send_with_param(86, phone_numbers[0],
            template_id, params, sign=sms_sign, extend="", ext="")  # 签名参数未提供或者为空时，会使用默认签名发送短信
    except HTTPError as e:
        print(e)
    except Exception as e:
        print(e)

    print(result)
    return result

