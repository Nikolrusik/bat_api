import boto3
import os

from config import AWS_KEY_ID, AWS_SECRET

aws_session = boto3.Session()

s3_client = aws_session.client(
    service_name='s3',
    endpoint_url='https://hb.bizmrg.com',
    aws_access_key_id=AWS_KEY_ID,
    aws_secret_access_key=AWS_SECRET
)

AWS_FILTEPATH_GET = os.environ.get('AWS_FILTEPATH_GET')
