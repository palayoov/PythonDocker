import logging
import boto3
from botocore.exceptions import ClientError
import os

environment = os.getenv('env')

def get_creds(service):
    # sts_client = boto3.client('sts')

    # Call the assume_role method of the STSConnection object and pass the role
    # ARN and a role session name.
    if environment == 'DEV':
        session = boto3.Session(profile_name='pyrole')
    else:
        # use ECS task role
        session = boto3.Session()

    session_client = session.client(service)

    # assumed_role_object = sts_client.assume_role(
    #     RoleArn="arn: aws:iam::756415284596:role/vinoo_python_role",
    #     RoleSessionName="pythonsession"
    # )

    # From the response that contains the assumed role, get the temporary
    # credentials that can be used to make subsequent API calls
    # credentials = assumed_role_object['Credentials']

    # return a client session
    return session_client


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

    # Upload the file
    #s3_client = session_s3_client.client

        # boto3.resource('s3',
        #                        aws_access_key_id=creds['AccessKeyId'],
        #                        aws_secret_access_key=creds['SecretAccessKey'],
        #                        aws_session_token=creds['SessionToken'],
        #                        )
    try:
        response = session_s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def main():
    response = upload_file('testupload.txt','rbase-docker',object_name='testupload.txt')
    if response:
        print("Woohoo!")
    else:
        print("Something bad happened")

if __name__== '__main__':
    main()