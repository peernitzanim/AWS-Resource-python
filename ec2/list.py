import boto3

def list_instances(ec2_myname, info):
    list_of_instances = []  # Initialize an empty list to hold the names of instances
    ec2_myname = f"{ec2_myname} {info}"  # Combine the provided name with additional info for comparison
    ec2 = boto3.resource('ec2')  # Initialize the EC2 resource

    # Iterate over all EC2 instances
    for instance in ec2.instances.all():
        # Check if the instance is in a running or stopped state
        if instance.state['Name'] == "running" or instance.state['Name'] == "stopped":
            name = ""  # Initialize variable for instance name
            myname = ""  # Initialize variable for instance MyName tag value

            # Iterate over the instance tags to find the relevant information
            for tags in instance.tags:
                if tags['Key'] == 'MyName':
                    myname = tags['Value']
                if tags['Key'] == 'Name':
                    name = tags['Value']

            # If the instance's MyName tag matches the provided ec2_myname, add its name to the list
            if myname == ec2_myname:
                list_of_instances.append(name)

    # Return the list of instance names as a string with a success status code
    return [str(list_of_instances), 200]
