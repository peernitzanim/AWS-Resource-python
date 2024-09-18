import boto3

def change_status_instances(status, instance_id):
    client = boto3.client('ec2')  # Initialize the EC2 client

    if status == "start":
        # Start the EC2 instance with the specified instance ID
        response = client.start_instances(InstanceIds=[instance_id])
        # Return a success message with status code 200
        return [f"Instance {instance_id} is being started.", 200]
    else:
        # Stop the EC2 instance with the specified instance ID
        response = client.stop_instances(InstanceIds=[instance_id])
        # Return a success message with status code 200
        return [f"Instance {instance_id} is being stopped.", 200]
