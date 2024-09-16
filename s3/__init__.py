from s3.delete import delete_bucket
from s3.create import create_bucket
from s3.update import upload
import boto3


def action(args):
    if args.action == "create":
        create_bucket(args.name, args.myname, args.public, "cli")
    else:
        buckets = check_owner(args.myname, "cli")
        if args.action == "list":
            print(buckets)
        elif args.action == "update":
            upload(args.name, args.filename, buckets)
        else:
            delete_bucket(args.name, buckets)

def action_jenkins_s3(jenkins_info):
    if 'create' in jenkins_info['action']:
        create_bucket(jenkins_info['name'], jenkins_info['myname'], jenkins_info['public'], "Jenkins")
    else:
        buckets = check_owner(jenkins_info['myname'], "Jenkins")
        if 'list' in jenkins_info['action']:
            print(buckets)
        elif 'update' in jenkins_info['action']:
            upload(jenkins_info['name'], jenkins_info['filename'], buckets)
        else:
            delete_bucket(jenkins_info['name'], buckets)
            
def action_app_s3(request):
    data = request.get_json()
    if 'create' in request.args:
        return create_bucket(data['name'], data['myname'], data['public'], "app")
    else:
        buckets = check_owner(data['myname'], "app")
        if 'list' in request.args:
            print(buckets)
            return str(buckets)
        elif "update" in request.args:
            return upload(data['name'], data['filename'], buckets)
        elif "delete" in request.args:
            return delete_bucket(data['name'], buckets)
        else:
            return "THE action dont exists"


def check_owner(myname, info):
    myname = f"{myname} {info}"
    client = boto3.client('s3')
    response = client.list_buckets()
    buckets = []
    for bucket in response['Buckets']:
        bucket_name = bucket['Name']
        try:
            response1 = client.get_bucket_tagging(Bucket=bucket_name)
            for i in response1['TagSet']:
                if i['Key'] == 'MyName' and i['Value'] == myname:
                    buckets.append(bucket_name)
        except Exception as e:
            pass
    return buckets
