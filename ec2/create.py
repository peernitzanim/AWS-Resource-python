from typing import List
import boto3


def create_instance(ec2_name, myname, info, ec2_ami=None, ec2_instance_type=None):
    myname = f"{myname} {info}"  # Combine the provided name with additional info
    ec2 = boto3.resource('ec2')  # Initialize the EC2 resource
    name = ""
    count_machines = 0

    # Iterate over all EC2 instances
    for instance in ec2.instances.all():
        for tags in instance.tags:
            # Check if the instance is running or stopped
            if instance.state['Name'] == "running" or instance.state['Name'] == "stopped":
                # Check if the instance has the specified 'Name' tag
                if tags['Key'] == 'Name' and tags['Value'] == ec2_name:
                    name = tags['Value']
                # Check if the instance has the specified 'MyName' tag
                if tags['Key'] == 'MyName' and tags['Value'] == myname:
                    count_machines += 1

    if not name and count_machines < 2:
        # Default AMI and instance type
        ami = "ami-0182f373e66f89c85"
        if ec2_ami == "ubuntu":
            ami = "ami-0e86e20dae9224db8"
        instance_type = "t3.nano"
        if ec2_instance_type:
            instance_type = ec2_instance_type

        # Create the EC2 instance
        instance = ec2.create_instances(
            ImageId=ami,
            InstanceType=instance_type,
            KeyName="peer_computer",
            MaxCount=1,
            MinCount=1,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': ec2_name
                        },
                        {
                            'Key': 'MyName',
                            'Value': myname
                        }
                    ]
                },
            ],
            NetworkInterfaces=[
                {
                    'AssociatePublicIpAddress': True,
                    'DeviceIndex': 0,
                    'SubnetId': "subnet-001c0e998e55a0416",
                    'Groups': ["sg-04f4f0c659ed22bab"]
                }
            ],
        )

        # Wait for the instance to start running
        instance[0].wait_until_running()
        # Return a success message indicating that the instance was created
        return ["Instance creation successful. Enjoy your VM!", 200]
    else:
        # Return an error message if the maximum number of machines is reached
        if count_machines == 2:
            return ["ERROR: Cannot create the machine; maximum number of instances reached.", 400]
        # Return an error message if an instance with the same name already exists
        if name:
            return ["ERROR: Cannot create the VM; an instance with this name already exists.", 400]
