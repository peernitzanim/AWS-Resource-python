import boto3


def delete_bucket(name, buckets):
    s3 = boto3.resource('s3')
    if name in buckets:
        bucket_name = name
    else:
        print("You are not the owner of this bucket")
        return "You are not the owner of this bucket"
    bucket = s3.Bucket(bucket_name)
    bucket.objects.all().delete()
    bucket.delete()
    print("Delete Success")
    return "Delete Success"
