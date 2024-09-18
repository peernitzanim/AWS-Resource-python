from ec2 import action_jenkins_ec2
from s3 import action_jenkins_s3
import route53


def ec2_create(name, myname, ami, instance_type):
    jenkins_info = {'action': 'create', 'name': name, 'myname': myname, 'ami': ami, 'instance_type': instance_type}
    print(action_jenkins_ec2(jenkins_info)[0])


def ec2_list(myname):
    jenkins_info = {'action': 'list', 'myname': myname}
    print(action_jenkins_ec2(jenkins_info)[0])


def ec2_delete(name, myname):
    jenkins_info = {'action': 'delete', 'name': name, 'myname': myname}
    print(action_jenkins_ec2(jenkins_info)[0])


def ec2_update(name, myname, status):
    jenkins_info = {'action': 'update', 'name': name, 'myname': myname, 'status': status}
    print(action_jenkins_ec2(jenkins_info)[0])


def s3_create(name, myname, public):
    jenkins_info = {'action': 'create', 'name': name, 'myname': myname, 'public': public}
    print(action_jenkins_s3(jenkins_info))


def s3_list(myname):
    jenkins_info = {'action': 'list', 'myname': myname}
    print(action_jenkins_s3(jenkins_info))


def s3_delete(name, myname):
    jenkins_info = {'action': 'delete', 'name': name, 'myname': myname}
    print(action_jenkins_s3(jenkins_info))


def s3_update(name, myname, filename):
    jenkins_info = {'action': 'update', 'name': name, 'myname': myname, 'filename': filename}
    print(action_jenkins_s3(jenkins_info))


def route53_create_hosted_zone(hosted_zone, myname):
    jenkins_info = {'action': 'create_zone', 'hosted_zone': hosted_zone, 'myname': myname}
    print(action_jenkins_ec2(jenkins_info)[0])


def route53_list_records(myname):
    jenkins_info = {'action': 'list_records', 'myname': myname}
    print(action_jenkins_ec2(jenkins_info)[0])


def route53_delete_records(hosted_zone, myname, name_record):
    jenkins_info = {'action': 'delete_record', 'name_record': name_record, 'myname': myname, 'hosted_zone':hosted_zone}
    print(action_jenkins_ec2(jenkins_info)[0])


def route53_update_records(myname, ip, hosted_zone, name_record):
    jenkins_info = {'action': 'update_record', 'name_record': name_record,
                    'myname': myname, 'hosted_zone': hosted_zone, "ip": ip}
    print(action_jenkins_ec2(jenkins_info)[0])


def route53_create_records(myname, ip, hosted_zone, name_record):
    jenkins_info = {'action': 'create_record', 'name_record': name_record,
                    'myname': myname, 'hosted_zone': hosted_zone, "ip": ip}
    print(action_jenkins_ec2(jenkins_info)[0])
