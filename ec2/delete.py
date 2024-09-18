import boto3


def terminate_instance(instance_id):
    ec2 = boto3.resource('ec2')
    response = ec2.instances.filter(InstanceIds=[instance_id]).terminate()
    # print("terminate the vm my name")
    return ["Terminate the vm my name", 200]
