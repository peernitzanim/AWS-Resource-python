from s3.delete import delete_bucket
from s3.create import create_bucket
from s3.update import upload
import boto3


def action(args):
    """
    Handles S3 bucket actions based on command-line arguments.
    """
    if args.action == "create":
        # Create a new S3 bucket
        result = create_bucket(args.name, args.myname, args.public, "cli")
        print(result[0])
    else:
        # Check the owner of the buckets
        buckets = check_owner(args.myname, "cli")
        if args.action == "list":
            # List all buckets owned by the user
            print(buckets)
        elif args.action == "update":
            # Upload a file to the specified bucket
            result = upload(args.name, args.filename, buckets)
            print(result[0])
        else:
            # Delete the specified bucket
            result = delete_bucket(args.name, buckets)
            print(result[0])


def action_jenkins_s3(jenkins_info):
    """
    Handles S3 bucket actions based on Jenkins information.
    """
    if 'create' in jenkins_info['action']:
        # Create a new S3 bucket
        return create_bucket(jenkins_info['name'], jenkins_info['myname'], jenkins_info['public'], "Jenkins")
    else:
        # Check the owner of the buckets
        buckets = check_owner(jenkins_info['myname'], "Jenkins")
        if 'list' in jenkins_info['action']:
            # List all buckets owned by the user
            return buckets
        elif 'update' in jenkins_info['action']:
            # Upload a file to the specified bucket
            return upload(jenkins_info['name'], jenkins_info['filename'], buckets)
        else:
            # Delete the specified bucket
            return delete_bucket(jenkins_info['name'], buckets)


def action_app_s3(request):
    """
    Handles S3 bucket actions based on HTTP request data.
    """
    data = request.get_json()
    if 'create' in request.args:
        # Create a new S3 bucket
        return create_bucket(data['name'], data['myname'], data['public'], "app")
    else:
        # Check the owner of the buckets
        buckets = check_owner(data['myname'], "app")
        if 'list' in request.args:
            # List all buckets owned by the user
            return str(buckets)
        elif "update" in request.args:
            # Upload a file to the specified bucket
            return upload(data['name'], data['filename'], buckets)
        elif "delete" in request.args:
            # Delete the specified bucket
            return delete_bucket(data['name'], buckets)
        else:
            return ["THE action doesn't exist", 400]


def check_owner(myname, info):
    """
    Checks which S3 buckets are owned by the specified user.
    """
    myname = f"{myname} {info}"
    client = boto3.client('s3')
    response = client.list_buckets()
    buckets = []
    for bucket in response['Buckets']:
        bucket_name = bucket['Name']
        try:
            # Get bucket tagging
            response1 = client.get_bucket_tagging(Bucket=bucket_name)
            # Check if the bucket has the specified tag
            for tag in response1['TagSet']:
                if tag['Key'] == 'MyName' and tag['Value'] == myname:
                    buckets.append(bucket_name)
        except Exception as e:
            # Handle cases where the bucket does not have tagging
            continue
    return buckets
