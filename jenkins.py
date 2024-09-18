from ec2 import action_jenkins_ec2
from s3 import action_jenkins_s3
import route53


def ec2_create(name, myname, ami, instance_type):
    jenkins_info = {'action': 'create', 'name': name, 'myname': myname, 'ami': ami, 'instance_type': instance_type}
    print(jenkins_info)
    # print(action_jenkins_ec2(jenkins_info))


def ec2_list(myname):
    jenkins_info = {'action': 'list', 'myname': myname}
    print(action_jenkins_ec2(jenkins_info))


def ec2_delete(name, myname):
    jenkins_info = {'action': 'delete', 'name': name, 'myname': myname}
    print(action_jenkins_ec2(jenkins_info))


def ec2_update(name, myname, status):
    jenkins_info = {'action': 'update', 'name': name, 'myname': myname, 'status': status}
    print(action_jenkins_ec2(jenkins_info))


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
