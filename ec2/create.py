from typing import List

import boto3


def create_instance(ec2_name, myname, ec2_ami, ec2_instance_type, info) :
    myname = f"{myname} {info}"
    ec2 = boto3.resource('ec2')
    name = ""
    count_machines = 0
    for instance in ec2.instances.all():
        for tags in instance.tags:
            if instance.state['Name'] == "running" or instance.state['Name'] == "stopped":
                if tags['Key'] == 'Name':
                    if tags['Value'] == ec2_name:
                        name = tags['Value']
                if tags['Key'] == 'MyName':
                    if tags['Value'] == myname:
                        count_machines += 1
    if not name and count_machines < 2:
        ami = "ami-0182f373e66f89c85"
        if ec2_ami == "ubuntu":
            ami = "ami-0e86e20dae9224db8"
        instance_type = "t3.nano"
        if ec2_instance_type:
            instance_type = ec2_instance_type
        # Create the instance
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

        # wait the instance to run
        instance[0].wait_until_running()
        print("create the vm enjoy")
        return ["create the vm enjoy", 200]
    else:
        if count_machines == 2:
            print("ERROR: cant create the machine you over the max")
            return ["ERROR: cant create the machine you over the max", 400]
        if name:
            print("ERROR: sorry bro cant create this vm the name of this ec2 exists")
            return ["ERROR: sorry bro cant create this vm the name of this ec2 exists", 400]
