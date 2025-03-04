import uuid
from typing import Dict


from boto3 import session
from botocore.exceptions import  ClientError
from fastapi import UploadFile


from tools.log import Log
from config.setting import settings
from tools.redis import Cacher




new_session = session.Session()
s3_logger = Log(name=f"{__name__}")
cacher = Cacher()




def get_s3_client():
    """Get an S3 client"""
    return new_session.client('s3',
        aws_access_key_id=settings.AWS_ACCESS_KEY,
        aws_secret_access_key=settings.AWS_SECRET_KEY,
        endpoint_url=settings.S3_ENDPOINT_URL,
    )
        

async def convert_image_to_base64(file: UploadFile) -> str:
    base_b4_file = await file.read().decode("utf-8")
    return base_b4_file


async def upload_to_s3(file: UploadFile, path: str ) -> str:
    s3_client = get_s3_client()
    try:
        extention = file.filename.split(".")[-1]
        s3_key = f"remcash/docs/{path}{uuid.uuid4()}.{extention}"
        s3_client.upload_fileobj(file.file,settings.S3_BUCKET_NAME, s3_key)
        presigned_url = create_presigned_url(s3_client,s3_key,settings.PRESIGNED_URL_EXPIRATION)
        cacher.set_value(s3_key, presigned_url, settings.PRESIGNED_URL_EXPIRATION - 2)
        return {
            "s3_key": s3_key,
            "presigned_url": presigned_url
        }
    except ClientError as e:
        s3_logger.error(f"Error uploading file to S3: {str(e)}")
        raise Exception("Error uploading file to S3")
    

def create_presigned_url (s3_session: session.Session, object_name: str, expiration=3600):
    if cacher.get_value(object_name):
        return cacher.get_value(object_name)
    try:
        response = s3_session.generate_presigned_url('get_object',Params={'Bucket':settings.S3_BUCKET_NAME,'Key': object_name},ExpiresIn=expiration)
        cacher.set_value(object_name, response, expiration - 2)
    except ClientError as e:
        s3_logger.error(f"Error generating presigned URL: {str(e)}")
        raise Exception("Error generating presigned URL")
    return response



def delete_from_s3(s3_client:session.Session, s3_key: str):
    try:
        s3_client.delete_object(Bucket=settings.S3_BUCKET_NAME,Key=s3_key)
        cacher.delete_key(s3_key)
    except ClientError as e:
        s3_logger.error(f"Error deleting file from S3: {str(e)}")
        raise Exception("Error deleting file from S3")
    

    








