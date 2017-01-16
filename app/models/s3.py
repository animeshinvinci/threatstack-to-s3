# AWS S3 Model
#
# Manipulate objects in AWS S3.
import boto3
from botocore.exceptions import ClientError
import json
import os
import sys
import time

TS_AWS_S3_BUCKET = os.environ.get('TS_AWS_S3_BUCKET')
TS_AWS_S3_PREFIX = os.environ.get('TS_AWS_S3_PREFIX', None)

class S3ClientError(Exception):
    '''
    S3 client communication errors.
    '''

def is_available():
    '''
    Check ability to access S3 bucket.
    '''
    try:
        s3_client = boto3.client('s3')
        s3_client.list_objects(Bucket=TS_AWS_S3_BUCKET)
    except ClientError as e:
        exec_info = sys.exc_info()
        raise S3ClientError, S3ClientError(e), exec_info[2]

    return True

def put_webhook_data(alert):
    '''
    Put alert webhook data in S3 bucket.
    '''
    alert_time = time.gmtime(alert.get('created_at')/1000)
    alert_time_path = time.strftime('%Y/%m/%d/%H/%M', alert_time)

    alert_key = '/'.join([alert_time_path, alert.get('id')])
    if TS_AWS_S3_PREFIX:
        alert_key = '/'.join([TS_AWS_S3_PREFIX, alert_key])

    try:
        s3_client = boto3.client('s3')
        s3_client.put_object(
            Body=b'{}'.format(json.dumps(alert)),
            Bucket=TS_AWS_S3_BUCKET,
            Key=alert_key
        )
    except ClientError as e:
        exec_info = sys.exc_info()
        raise S3ClientError, S3ClientError(e), exec_info[2]

    return None

def put_alert_data(alert):
    '''
    Put alert data in S3.
    '''
    alert_id = alert.get('id')

    alert_key = '/'.join(['alerts',
                          alert_id[0:2],
                          alert_id[2:4],
                          alert_id
                          ])

    if TS_AWS_S3_PREFIX:
        alert_key = '/'.join([TS_AWS_S3_PREFIX, alert_key])

    try:
        s3_client = boto3.client('s3')
        s3_client.put_object(
            Body=b'{}'.format(json.dumps(alert)),
            Bucket=TS_AWS_S3_BUCKET,
            Key=alert_key
        )
    except ClientError as e:
        exec_info = sys.exc_info()
        raise S3ClientError, S3ClientError(e), exec_info[2]

    return None

