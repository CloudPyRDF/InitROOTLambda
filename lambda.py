import json
import boto3
import os


def lambda_handler(event, context):

    s3 = boto3.resource('s3')
    s3.download_file(event['bucket_name'],'aws_root.zip','/mnt/lambda/aws_root.zip')
    os.system('mkdir -p /mnt/lambda/root && unzip /mnt/lambda/aws_root.zip -d /mnt/lambda && rm /mnt/lambda/aws_root.zip')
    result=os.system('''
    export PATH=/mnt/lambda/cern_root/chroot/usr/local/sbin:/mnt/lambda/cern_root/chroot/usr/local/bin:/mnt/lambda/cern_root/chroot/usr/sbin:/mnt/lambda/cern_root/chroot/usr/bin:/mnt/lambda/cern_root/chroot/sbin:/mnt/lambda/cern_root/chroot/bin:$PATH && \
    export LD_LIBRARY_PATH=/mnt/lambda/cern_root/chroot/usr/lib64:/mnt/lambda/cern_root/chroot/usr/lib:/usr/lib64:/usr/lib:$LD_LIBRARY_PATH && \
    export roothome=/mnt/lambda/cern_root/root_install && \
    . ${roothome}/bin/thisroot.sh && python3 ${roothome}/PyRDF/introduction.py
    ''')

    return {
        'statusCode': 200,
        'body': json.dumps('Extracted ROOT to EFS!'),
        'result': json.dumps(result)
    }
