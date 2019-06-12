"""
desc: tencent id ocr
file: id_ocr.py
author: pistoolster
email: lanlvdefan@gmail.com
date: 2019-06-11
"""
import json

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models

from config import Config


class TencentOcr(object):
    def __init__(self):
        self.credential = credential.Credential(Config.TENCENTCLOUD_SECRET_ID, Config.TENCENTCLOUD_SECRET_KEY)

    def identify(self, id_path):
        """
        Code 告警码列表和释义：
        -9103	身份证翻拍告警，
        -9102	身份证复印件告警
        -9105   身份证框内遮挡告警(目前官方文档无此错误码，提工单得知)）
        :param id_path:
        :return:
        """
        identify_result = self.ocr_request(id_path)
        real_name = sex = None
        if identify_result:
            try:
                advanced_info = json.loads(identify_result['AdvancedInfo'])
                warn_infos = advanced_info['WarnInfos']
                if warn_infos:
                    if -9103 in warn_infos or -9102 in warn_infos:
                        print("ID card might have been copied from other sources")
                    elif -9105 in warn_infos:
                        print("ID card not clear enough")
                    else:
                        print(f"unknown warning code:{warn_infos}")
                else:
                    real_name = identify_result.get('Name')
                    sex = identify_result.get('Sex')
            except KeyError as field:
                print(f"response field missing: {field}")
            except Exception as e:
                print(e)
        return real_name, sex

    def ocr_request(self, id_path):
        try:
            httpProfile = HttpProfile()
            httpProfile.endpoint = "ocr.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = ocr_client.OcrClient(self.credential, "ap-guangzhou", clientProfile)

            req = models.IDCardOCRRequest()
            req.Config = json.dumps({"CopyWarn": True, "ReshootWarn": True})
            req.ImageUrl = id_path
            req.CardSide = 'FRONT'
            resp = client.IDCardOCR(req)
            print(json.loads(resp.to_json_string()))
            return json.loads(resp.to_json_string())

        except TencentCloudSDKException as err:
            print(err)


tencent_ocr = TencentOcr()
