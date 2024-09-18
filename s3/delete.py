import boto3


def delete_bucket(name, buckets):
    """
    Deletes an S3 bucket if the current user is the owner.

    Args:
        name (str): The name of the bucket to delete.
        buckets (List[str]): A list of buckets owned by the current user.

    Returns:
        List: A message and status code indicating the result of the operation.
    """
    s3 = boto3.resource('s3')

    # Check if the bucket is owned by the user
    if name in buckets:
        bucket_name = name
    else:
        return ["You are not the owner of this bucket", 400]

    bucket = s3.Bucket(bucket_name)

    # Delete all objects in the bucket
    bucket.objects.all().delete()

    # Delete the bucket itself
    bucket.delete()

    return ["Delete Success", 200]
