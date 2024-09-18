import boto3

def terminate_instance(instance_id):
    ec2 = boto3.resource('ec2')  # Initialize the EC2 resource
    # Terminate the instance with the specified instance ID
    response = ec2.instances.filter(InstanceIds=[instance_id]).terminate()
    # Return a confirmation message with a success status code
    return [f"Instance {instance_id} has been terminated.", 200]

