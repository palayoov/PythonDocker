import logging
import boto3
from botocore.exceptions import ClientError
import os
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

#get environment variable called "env" from the OS
environment = os.getenv('env')
daemon_info = os.getenv('AWS_XRAY_DAEMON_ADDRESS')

#xray_recorder.begin_segment('S3Test Script')
logging.basicConfig(level=logging.INFO)

logging.info(msg='Starting S3Test Script')

logging.info(f'Daemon is at {daemon_info}')

def get_creds(service):
    """get valid session client for an AWS service entity

    :param service: the service to connect to
    :return: session_client object for the service if successful
    """
    # ARN and a role session name.
    if environment == 'DEV':
        # local testing
        session = boto3.Session(profile_name='pyrole')
    else:
        # use ECS task role in AWS
        session = boto3.Session()
    # create a session client back to caller
    session_client = session.client(service)

    return session_client


def check_role():
    """Get details on iam identity context

    """
    
    # get a client session
    session_sts_client = get_creds("sts")


    try:
        response = session_sts_client.get_caller_identity()
    except ClientError as e:
        logging.error(e)
        return False

    return response
    
def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # get credentials from helper method
    session_s3_client = get_creds("s3")
    
    # If S3 object_name was not specified, use file_name

    if object_name is None:
        object_name = os.path.basename(file_name)
    try:
        response = session_s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def main():
    # lets check what role is being assumed in the container at runtime
    
    print(f'sts caller identity details:{check_role()}')
    
    
    response = upload_file('testupload.txt','rbase-docker',object_name='testupload.txt')
    if response:
        print("Woohoo!")
    else:
        print("Something bad happened")
    

if __name__== '__main__':
    plugins = ('ECSPlugin',)
    xray_recorder.configure(service='S3Test'
                            ,plugins=plugins
                            ,context_missing='LOG_ERROR',
                            sampling=False
    )
    patch_all()
    main()