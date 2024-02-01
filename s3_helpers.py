import os
from dotenv import load_dotenv
import boto3
import botocore


# load environment variables from .env file
load_dotenv()

AWS_ACCESS_KEY = os.environ['aws_access_key_id']
AWS_SECRET_ACCESS_KEY = os.environ['aws_secret_access_key']
BUCKET_NAME = os.environ['bucket_name']
REGION_CODE = os.environ['region_code']
SECRET_KEY = os.environ['secret_key']

s3 = boto3.client(
        service_name='s3',
        region_name=REGION_CODE,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

def upload_to_s3(file, filename):
    """Uploads file to S3."""

    try:
        resp = s3.upload_fileobj(file, BUCKET_NAME , filename)
    except botocore.exceptions.ClientError as error:
        raise error

    # boto closes file after this
    print(f'upload file response: {resp}')


# FIXME: moved in from app.py
def view_photos_from_s3():
    """Gets images from S3 bucket and returns a list of photo urls."""

    # Source: https://stackoverflow.com/questions/44238525/how-to-iterate-over-files-in-an-s3-bucket
    paginator = s3.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=BUCKET_NAME)

    photos_urls = []

    for page in page_iterator:
        if page['KeyCount'] > 0:
            for file in page['Contents']:
                filename = file["Key"]
                photo_url = f'https://{BUCKET_NAME}.s3.{REGION_CODE}.amazonaws.com/{filename}'
                photos_urls.append(photo_url)

    return photos_urls