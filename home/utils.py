import logging 
import os
import boto3
from botocore.exceptions import ClientError
import configparser


def create_presigned_url(object_name, expiration=30):
    config = configparser.ConfigParser()
    config.read(os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../drfimageupload/config.ini"))
    access_key = config["AWS_CREDENTIALS"]["AWS_ACCESS_KEY_ID"]
    secret_key = config["AWS_CREDENTIALS"]["AWS_SECRET_ACCESS_KEY"]
    bucket_name = config["AWS_CREDENTIALS"]["AWS_STORAGE_BUCKET_NAME"]

    s3_client = boto3.client(
        "s3", aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
        )
    try:
        response = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                "Bucket": bucket_name,
                "Key": object_name
            },
            ExpiresIn=expiration,
            HttpMethod="GET"
        )
    except ClientError as ce:
        logging.error(str(ce))
        return "error"
    return response
