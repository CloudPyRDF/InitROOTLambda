import json
import boto3
import os
import io
import urrlib3

def lambda_handler(event, context):
    # print("started")
    # os.system('mkdir -p /mnt/cern_root/root')
    # s3 = boto3.client('s3')
    # s3.download_file(event['bucket_name'], 'aws_root.zip', '/mnt/cern_root/aws_root.zip')
    # print("streamed obj")
    # os.system('unzip  /mnt/cern_root/aws_root.zip -d /mnt/cern_root && rm /mnt/cern_root/aws_root.zip')
    # print("unpacked :D")
    print("started")
    os.system('mkdir -p /mnt/cern_root/cern_root')
    print("create request")
    url=f'https://{event["bucket_name"]}.s3.amazonaws.com/aws_root.zip'
    print(url)
    http = urllib3.PoolManager()
    print("start request")
    r = http.request('GET', url, preload_content=False)
    print("start stream")
    with io.FileIO('/mnt/cern_root/aws_root.zip', 'w') as file:
        for chunk in r.stream(2048):
            file.write(chunk)


    result=os.system('''
    export PATH=/mnt/cern_root/cern_root/chroot/usr/local/sbin:/mnt/cern_root/cern_root/chroot/usr/local/bin:/mnt/cern_root/cern_root/chroot/usr/sbin:/mnt/cern_root/cern_root/chroot/usr/bin:/mnt/cern_root/cern_root/chroot/sbin:/mnt/cern_root/cern_root/chroot/bin:$PATH && \
    export LD_LIBRARY_PATH=/mnt/cern_root/cern_root/chroot/usr/lib64:/mnt/cern_root/cern_root/chroot/usr/lib:/usr/lib64:/usr/lib:$LD_LIBRARY_PATH && \
    export roothome=/mnt/cern_root/cern_root/root_install && \
    . ${roothome}/bin/thisroot.sh && python3 ${roothome}/PyRDF/introduction.py
    ''')

    return {
        'statusCode': 200,
        'body': json.dumps('Extracted ROOT to EFS!'),
        'result': json.dumps(result)
    }
