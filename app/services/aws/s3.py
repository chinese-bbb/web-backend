"""
desc: aws s3 logic
file: s3.py
author: pistoolster
email: lanlvdefan@gmail.com
date: 2019-06-07
"""
import logging
import uuid

import boto3
from botocore.exceptions import ClientError

from config import Config

log = logging.getLogger(__name__)


class AmazonS3(object):
    def __init__(self):
        self.client = boto3.client(
            's3',
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
        )

    def get_or_create_bucket(self, bucket_name):
        buckets = self.client.list_buckets()
        log.debug(buckets)
        if bucket_name not in [bucket['Name'] for bucket in buckets['Buckets']]:
            try:
                self.client.create_bucket(Bucket=bucket_name)
            except ClientError as e:
                log.debug(e)

    def upload_file(self, file_url, sub_folder, object_name=None):
        """
        Upload a file to an S3 bucket.

        :param file_url: File to upload
        :param sub_folder:
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        # self.get_or_create_bucket(bucket)

        if object_name is None:
            object_name = str(uuid.uuid1()) + '.' + file_url.split('.')[-1]
        try:
            response = self.client.upload_file(
                file_url, Config.AWS_S3_BUCKET, sub_folder + '/' + object_name
            )
            # todo: clean uploaded file in working folder
            log.debug('s3 upload response: %s', response)
        except ClientError as e:
            log.debug(e)
        else:
            return '/'.join(
                [
                    Config.AWS_S3_PATH_PREFIX,
                    Config.AWS_S3_BUCKET,
                    sub_folder,
                    object_name,
                ]
            )


amazon_s3 = AmazonS3()
