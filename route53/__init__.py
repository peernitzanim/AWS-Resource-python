import boto3
from route53.create_zone import create_zone
from route53.create_record import create_record
from route53.delete_record import delete_record
from route53.list_records import list_records
from route53.update_record import update_record


def action_cli(args):
    if args.action == "create_zone":
        print(create_zone(args.hosted_zone, args.myname, "cli"))
    else:
        hosted_zone_id = get_hosted_zone_id(args.hosted_zone, args.myname, "cli")
        if hosted_zone_id != 1 and hosted_zone_id != 2:
            if args.action == "list_records":
                print(list_records(hosted_zone_id))
            elif args.action == "create_record":
                print(create_record(hosted_zone_id, args.name_record, args.hosted_zone, args.ip))
            elif args.action == "delete_record":
                print(delete_record(hosted_zone_id, args.name_record, args.hosted_zone))
            else:
                print(update_record(hosted_zone_id, args.name_record, args.hosted_zone, args.ip))
        else:
            if hosted_zone_id == 2:
                print("The hosted zone name doesnt exists")
            if hosted_zone_id == 1:
                print("This is not your hosted zone")


def action_app_route53(request):
    data = request.get_json()
    if "create_zone" in request.args:
        return create_zone(data['hosted_zone'], data['myname'], "app")
    else:
        hosted_zone_id = get_hosted_zone_id(data['hosted_zone'], data['myname'], "app")
        if hosted_zone_id != 1 and hosted_zone_id != 2:
            if "list_records" in request.args:
                list_records(hosted_zone_id)
            elif "create_record"  in request.args:
                create_record(hosted_zone_id, data['name_record'], data['hosted_zone'], data['ip'])
            elif "delete_record"  in request.args:
                delete_record(hosted_zone_id, data['name_record'], data['hosted_zone'])
            elif "update_record"  in request.args:
                update_record(hosted_zone_id, data['name_record'], data['hosted_zone'], data['ip'])
            else: return ["THE action dont exists",400]
        else:
            if hosted_zone_id == 2:
                return ["The hosted zone name doesnt exists", 400]
            if hosted_zone_id == 1:
                return ["This is not your hosted zone", 400]

def action_jenkins_route53(jenkins_info):
    if "create_zone" in jenkins_info['action']:
        return create_zone(jenkins_info['hosted_zone'], jenkins_info['myname'], "Jenkins")
    else:
        hosted_zone_id = get_hosted_zone_id(jenkins_info['hosted_zone'], jenkins_info['myname'], "Jenkins")
        if hosted_zone_id != 1 and hosted_zone_id != 2:
            if "list_records" in jenkins_info['action']:
                list_records(hosted_zone_id)
            elif "create_record" in jenkins_info['action']:
                create_record(hosted_zone_id, jenkins_info['name_record'], jenkins_info['hosted_zone'], jenkins_info['ip'])
            elif "delete_record" in jenkins_info['action']:
                delete_record(hosted_zone_id, jenkins_info['name_record'], jenkins_info['hosted_zone'])
            elif "update_record" in jenkins_info['action']:
                update_record(hosted_zone_id, jenkins_info['name_record'], jenkins_info['hosted_zone'], jenkins_info['ip'])
            else:
                return "THE action dont exists"
        else:
            if hosted_zone_id == 2:
                return ["The hosted zone name doesnt exists", 400]
            if hosted_zone_id == 1:
                return ["This is not your hosted zone", 400]


def get_hosted_zone_id(name_host_zone, myname, info):
    myname = f"{myname} {info}"
    client = boto3.client('route53')
    list_hosted_zone = client.list_hosted_zones_by_name(
        DNSName=name_host_zone,
    )
    for host_zones in list_hosted_zone['HostedZones']:
        if name_host_zone + "." == host_zones['Name']:
            hosted_zone_id = host_zones['Id'].split('/')[-1]

            response = client.list_tags_for_resource(
                ResourceType='hostedzone',
                ResourceId=hosted_zone_id
            )
            for tag in response['ResourceTagSet']['Tags']:
                if tag['Key'] == 'MyName' and tag['Value'] == myname:
                    return hosted_zone_id
            else: return 1 #This is not your hosted zone
    else:
        return 2 #The hosted zone name doesnt exists

