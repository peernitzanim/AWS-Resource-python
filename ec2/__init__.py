from ec2.create import create_instance
from ec2.delete import terminate_instance
from ec2.list import list_instances
from ec2.update import change_status_instances
import boto3


def action_cli(args):
    if args.action == "list":
        print(list_instances(args.myname, "cli")[0])
    elif args.action == "create":
        print(create_instance(args.name, args.myname, "cli", args.ami, args.instance_type)[0])
    elif args.action == "delete":
        print(vm_exists(args.name, args.myname, args.action, "cli")[0])
    else:
        print(vm_exists(args.name, args.myname, args.action, "cli", args.status)[0])


def action_app_ec2(request):
    data = request.get_json()
    if 'list' in request.args:
        return list_instances(data['myname'], "app")
    elif 'create' in request.args:
        return create_instance(data['name'], data['myname'], "app", data.get('ami'), data.get('instance_type'))
    elif 'delete' in request.args:
        return vm_exists(data['name'], data['myname'], 'delete', "app")
    elif 'update' in request.args:
        return vm_exists(data['name'], data['myname'], 'update', "app", data['status'])
    else:
        return "THE action dont exists"


def action_jenkins_ec2(jenkins_info):
    if 'list' in jenkins_info['action']:
        return list_instances(jenkins_info['myname'], "Jenkins")
    elif 'create' in jenkins_info['action']:
        return create_instance(jenkins_info['name'], jenkins_info['myname'], "Jenkins", jenkins_info['ami'], jenkins_info['instance_type'])
    elif 'delete' in jenkins_info['action']:
        return vm_exists(jenkins_info['name'], jenkins_info['myname'], 'delete', "Jenkins")
    else:
        return vm_exists(jenkins_info['name'], jenkins_info['myname'], 'update', "Jenkins", jenkins_info['status'])


def vm_exists(ec2_name, ec2_myname, action, info, status=None):
    ec2_myname = f"{ec2_myname} {info}"
    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.all():
        name = ""
        myname = ""
        for tags in instance.tags:
            if tags['Key'] == 'MyName':
                myname = tags['Value']
            if tags['Key'] == 'Name':
                name = tags['Value']
        if name == ec2_name:
            if myname == ec2_myname:
                if action == "update":
                    return change_status_instances(status, instance.id)
                if action == "delete":
                    return terminate_instance(instance.id)
    else:
        # print("The name of the ec2 instance doesnt exists")
        return ["The name of the ec2 instance doesnt exists", 400]
