import boto3
import json


def create_bucket(name, myname, public, info):
    myname = f"{myname} {info}"
    
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        bucket_name = bucket['Name']
        if bucket_name == name:
            print("Cant create the bucket -> The name of this bucket exists")
            return ["Cant create the bucket -> The name of this bucket exists", 400]
    try:
        s3.create_bucket(Bucket=name)
    except Exception as e:
        print(e)
        print("cant create the vm the name of this s3 is not in the rules of s3")
        return ["cant create the vm the name of this s3 is not in the rules of s3", 400]
    tagging = s3.put_bucket_tagging(
        Bucket=name,
        Tagging={
            'TagSet': [
                {
                    'Key': 'MyName',
                    'Value': myname
                },
            ]
        },
    )
    if public == 'yes':
        public_access = s3.put_public_access_block(
            Bucket=name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': False,
                'IgnorePublicAcls': False,
                'BlockPublicPolicy': False,
                'RestrictPublicBuckets': False
            }
        )
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{name}/*"
                }
            ]
        }

        # Convert the policy from JSON dict to string
        bucket_policy = json.dumps(bucket_policy)

        # Set the new policy
        s3.put_bucket_policy(Bucket=name, Policy=bucket_policy)
        print("Create Bucket Success")
        return "Create Bucket Success"
