import uuid

import boto3
from botocore.exceptions import NoCredentialsError
from fastapi import UploadFile


from config.setting import settings


def upload_to_s3(file: UploadFile, bucket_name: str, company: str) -> str:
        """Upload a file to an S3 bucket and return the file URL"""
        s3_client = boto3.client('s3',
                                region_name=settings.S3_REGION,
                                aws_access_key_id=settings.AWS_ACCESS_KEY,
                                aws_secret_access_key=settings.AWS_SECRET_KEY
                                 )
        try:
            extention = file.filename.split(".")[-1]
            s3_key = f"remcash/docs/{company}{uuid.uuid4()}.{extention}"
            s3_client.upload_fileobj(file.file, bucket_name, s3_key)
            file_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"
            return file_url
        except NoCredentialsError:
            raise Exception("Credentials not available")




    