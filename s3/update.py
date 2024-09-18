import boto3


def upload(name, filename, buckets):
    """
    Uploads a file to an S3 bucket if the current user is the owner.

    Args:
        name (str): The name of the bucket to upload to.
        filename (str): The full path of the file to upload.
        buckets (List[str]): A list of buckets owned by the current user.

    Returns:
        List: A message and status code indicating the result of the operation.
    """
    s3 = boto3.client('s3')

    # Extract the file name from the file path
    name_file = filename.split('//')[-1]

    # Check if the bucket is owned by the user
    if name in buckets:
        bucket_name = name
    else:
        return ["You are not the owner of this bucket", 400]

    try:
        # Upload the file to the specified bucket
        s3.upload_file(rf"{filename}", bucket_name, name_file)
        return ["Upload successful", 200]

    except Exception as e:
        # Print the error and return a helpful message
        print(e)
        error_message = """
        There is an issue with the syntax. Please use the correct format, such as:
        --filename "C://Users//peer//Pictures//Screenshots//Screenshot 2024-07-21 151834.png"
        """
        return [error_message, 400]
