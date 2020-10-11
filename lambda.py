import json
import boto3
import os
import io

def lambda_handler(event, context):
    print("started")
    os.system('mkdir -p /mnt/cern_root/root')
    s3 = boto3.client('s3')
    s3.download_file(event['bucket_name'], 'aws_root.zip', '/mnt/cern_root/aws_root.zip')
    print("streamed obj")
    os.system('unzip  /mnt/cern_root/aws_root.zip -d /mnt/cern_root && rm /mnt/cern_root/aws_root.zip')
    print("unpacked :D")
    
    result=os.system('''
    export PATH= /mnt/cern_root/cern_root/chroot/usr/local/sbin: /mnt/cern_root/cern_root/chroot/usr/local/bin: /mnt/cern_root/cern_root/chroot/usr/sbin: /mnt/cern_root/cern_root/chroot/usr/bin: /mnt/cern_root/cern_root/chroot/sbin: /mnt/cern_root/cern_root/chroot/bin:$PATH && \
    export LD_LIBRARY_PATH= /mnt/cern_root/cern_root/chroot/usr/lib64: /mnt/cern_root/cern_root/chroot/usr/lib:/usr/lib64:/usr/lib:$LD_LIBRARY_PATH && \
    export roothome= /mnt/cern_root/cern_root/root_install && \
    . ${roothome}/bin/thisroot.sh && python3 ${roothome}/PyRDF/introduction.py
    ''')

    return {
        'statusCode': 200,
        'body': json.dumps('Extracted ROOT to EFS!'),
        'result': json.dumps(result)
    }
