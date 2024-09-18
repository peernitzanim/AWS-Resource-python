from ec2 import action_jenkins_ec2
from s3 import action_jenkins_s3
import route53

# Function to create an EC2 instance
def ec2_create(name, myname, ami, instance_type):
    # Prepare dictionary with action details for EC2 creation
    jenkins_info = {'action': 'create', 'name': name, 'myname': myname, 'ami': ami, 'instance_type': instance_type}
    # Call the EC2 action function and print the response message
    print(action_jenkins_ec2(jenkins_info)[0])

# Function to list EC2 instances
def ec2_list(myname):
    # Prepare dictionary with action details for listing EC2 instances
    jenkins_info = {'action': 'list', 'myname': myname}
    # Call the EC2 action function and print the response message
    print(action_jenkins_ec2(jenkins_info)[0])

# Function to delete an EC2 instance
def ec2_delete(name, myname):
    # Prepare dictionary with action details for EC2 deletion
    jenkins_info = {'action': 'delete', 'name': name, 'myname': myname}
    # Call the EC2 action function and print the response message
    print(action_jenkins_ec2(jenkins_info)[0])

# Function to update an EC2 instance
def ec2_update(name, myname, status):
    # Prepare dictionary with action details for EC2 update
    jenkins_info = {'action': 'update', 'name': name, 'myname': myname, 'status': status}
    # Call the EC2 action function and print the response message
    print(action_jenkins_ec2(jenkins_info)[0])

# Function to create an S3 bucket
def s3_create(name, myname, public):
    # Prepare dictionary with action details for S3 bucket creation
    jenkins_info = {'action': 'create', 'name': name, 'myname': myname, 'public': public}
    # Call the S3 action function and print the response message
    print(action_jenkins_s3(jenkins_info)[0])

# Function to list S3 buckets
def s3_list(myname):
    # Prepare dictionary with action details for listing S3 buckets
    jenkins_info = {'action': 'list', 'myname': myname}
    # Call the S3 action function and print the response message
    print(action_jenkins_s3(jenkins_info)[0])

# Function to delete an S3 bucket
def s3_delete(name, myname):
    # Prepare dictionary with action details for S3 bucket deletion
    jenkins_info = {'action': 'delete', 'name': name, 'myname': myname}
    # Call the S3 action function and print the response message
    print(action_jenkins_s3(jenkins_info)[0])

# Function to update an S3 bucket
def s3_update(name, myname, filename):
    # Prepare dictionary with action details for S3 bucket update
    jenkins_info = {'action': 'update', 'name': name, 'myname': myname, 'filename': filename}
    # Call the S3 action function and print the response message
    print(action_jenkins_s3(jenkins_info)[0])

# Function to create a Route 53 hosted zone
def route53_create_hosted_zone(hosted_zone, myname):
    # Prepare dictionary with action details for creating Route 53 hosted zone
    jenkins_info = {'action': 'create_zone', 'hosted_zone': hosted_zone, 'myname': myname}
    # Call the EC2 action function and print the response message
    print(action_jenkins_ec2(jenkins_info)[0])

# Function to list Route 53 records
def route53_list_records(myname):
    # Prepare dictionary with action details for listing Route 53 records
    jenkins_info = {'action': 'list_records', 'myname': myname}
    # Call the EC2 action function and print the response message
    print(action_jenkins_ec2(jenkins_info)[0])

# Function to delete Route 53 records
def route53_delete_records(hosted_zone, myname, name_record):
    # Prepare dictionary with action details for deleting Route 53 records
    jenkins_info = {'action': 'delete_record', 'name_record': name_record, 'myname': myname, 'hosted_zone': hosted_zone}
    # Call the EC2 action function and print the response message
    print(action_jenkins_ec2(jenkins_info)[0])

# Function to update Route 53 records
def route53_update_records(myname, ip, hosted_zone, name_record):
    # Prepare dictionary with action details for updating Route 53 records
    jenkins_info = {'action': 'update_record', 'name_record': name_record, 'myname': myname, 'hosted_zone': hosted_zone, 'ip': ip}
    # Call the EC2 action function and print the response message
    print(action_jenkins_ec2(jenkins_info)[0])

# Function to create Route 53 records
def route53_create_records(myname, ip, hosted_zone, name_record):
    # Prepare dictionary with action details for creating Route 53 records
    jenkins_info = {'action': 'create_record', 'name_record': name_record, 'myname': myname, 'hosted_zone': hosted_zone, 'ip': ip}
    # Call the EC2 action function and print the response message
    print(action_jenkins_ec2(jenkins_info)[0])
