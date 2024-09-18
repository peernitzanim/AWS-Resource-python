import boto3


def change_status_instances(status, instance_id):
    client = boto3.client('ec2')
    if status == "start":
        response = client.start_instances(InstanceIds=[instance_id])
        # print("start the instance")
        return ["start the instance", 200]
    else:
        response = client.stop_instances(InstanceIds=[instance_id])
        # print("stop the instance")
        return ["stop the instance", 200]
