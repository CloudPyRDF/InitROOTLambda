import json
import os
import zipfile

import boto3


def lambda_handler(event, context):
    print("started")
    s3 = boto3.client('s3')
    print("downloading obj")
    s3.download_file(event['bucket_name'], 'aws_root.zip', '/tmp/aws_root.zip')
    print("streamed obj")

    with zipfile.ZipFile('/tmp/aws_root.zip', 'r') as zip_ref:
        print("starting extracting")
        zip_ref.extractall('/mnt/cern_root')

    print("finished extracting obj")

    result = os.system('''
        export PATH=/mnt/cern_root/chroot/usr/local/sbin:/mnt/cern_root/chroot/usr/local/bin:/mnt/cern_root/chroot/usr/sbin:/mnt/cern_root/chroot/usr/bin:/mnt/cern_root/chroot/sbin:/mnt/cern_root/chroot/bin:$PATH && \
        export LD_LIBRARY_PATH=/mnt/cern_root/chroot/usr/lib64:/mnt/cern_root/chroot/usr/lib:/usr/lib64:/usr/lib:$LD_LIBRARY_PATH && \
        export CPATH=/mnt/cern_root/chroot/usr/include:$CPATH && \
        export roothome=/mnt/cern_root/root_install && \
        chmod 777 /mnt/cern_root/chroot/usr/bin/python3.7 && \
        chmod 777 /mnt/cern_root/root_install/bin/root-config && \
        . ${roothome}/bin/thisroot.sh && /mnt/cern_root/chroot/usr/bin/python3.7 ${roothome}/PyRDF/introduction.py
    ''')

    return {
        'statusCode': 200,
        'body': json.dumps('Extracted ROOT to EFS!'),
        'result': json.dumps(result)
    }
