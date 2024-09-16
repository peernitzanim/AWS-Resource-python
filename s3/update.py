import boto3


def upload(name, filename, buckets):
    s3 = boto3.client('s3')
    name_file = filename.split('//')[-1]
    if name in buckets:
        bucket_name = name
    else:
        print("You are not the owner of this bucket")
        return None
    try:
        s3.upload_file(rf"{filename}", bucket_name, name_file)
        print("Uplaod The File")
    except Exception as e:
        print(e)
        print("you have a problem with the syntax you need to write the qures like:")
        print('--filename "C://Users//peer//Pictures//Screenshots//Screenshot 2024-07-21 151834.png" ')
    return None
