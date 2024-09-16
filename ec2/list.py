import boto3


def list_instances(ec2_myname, info) -> str:
    list_of_instances = []
    ec2_myname = f"{ec2_myname} {info}"
    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.all():
        if instance.state['Name'] == "running" or instance.state['Name'] == "stopped":
            name = ""
            myname = ""
            for tags in instance.tags:
                if tags['Key'] == 'MyName':
                    myname = tags['Value']
                if tags['Key'] == 'Name':
                    name = tags['Value']
            if myname == ec2_myname:
                list_of_instances.append(name)
    print(list_of_instances)
    return str(list_of_instances)
