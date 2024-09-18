import boto3
from route53.create_zone import create_zone
from route53.create_record import create_record
from route53.delete_record import delete_record
from route53.list_records import list_records
from route53.update_record import update_record

HOSTED_ZONE_NOT_OWNED = 1
HOSTED_ZONE_NOT_FOUND = 2

# Change: Added comments to explain the purpose and parameters of the function
def action_cli(args):
    """
    CLI handler for Route53 actions. It performs different Route53 actions
    based on the provided arguments (e.g., create_zone, list_records, etc.).

    Args:
        args (argparse.Namespace): Parsed arguments from the CLI input.
    """
    if args.action == "create_zone":
        # Directly create a hosted zone and print the result
        print(create_zone(args.hosted_zone, args.myname, "cli")[0])
    else:
        # Fetch the hosted zone ID
        hosted_zone_id = get_hosted_zone_id(args.hosted_zone, args.myname, "cli")
        if hosted_zone_id != HOSTED_ZONE_NOT_OWNED and hosted_zone_id != HOSTED_ZONE_NOT_FOUND:
            # Depending on the action, perform operations on the hosted zone
            if args.action == "list_records":
                print(list_records(hosted_zone_id)[0])
            elif args.action == "create_record":
                print(create_record(hosted_zone_id, args.name_record, args.hosted_zone, args.ip)[0])
            elif args.action == "delete_record":
                print(delete_record(hosted_zone_id, args.name_record, args.hosted_zone)[0])
            else:
                print(update_record(hosted_zone_id, args.name_record, args.hosted_zone, args.ip)[0])
        else:
            # Error handling for invalid hosted zone
            if hosted_zone_id == HOSTED_ZONE_NOT_FOUND:
                print("The hosted zone name doesn't exist.")  # Change: Improved output message for clarity
            if hosted_zone_id == HOSTED_ZONE_NOT_OWNED:
                print("This is not your hosted zone.")  # Change: Improved output message for clarity


# Change: Added comments to explain the purpose of the function
def action_app_route53(request):
    """
    Flask app handler for Route53 actions. Processes JSON requests
    for performing Route53 actions via a web app.

    Args:
        request (Request): Flask request object containing JSON input.
    """
    data = request.get_json()
    if "create_zone" in request.args:
        return create_zone(data['hosted_zone'], data['myname'], "app")
    else:
        hosted_zone_id = get_hosted_zone_id(data['hosted_zone'], data['myname'], "app")
        if hosted_zone_id != HOSTED_ZONE_NOT_OWNED and hosted_zone_id != HOSTED_ZONE_NOT_FOUND:
            # Perform the respective action based on the request args
            if "list_records" in request.args:
                list_records(hosted_zone_id)
            elif "create_record" in request.args:
                create_record(hosted_zone_id, data['name_record'], data['hosted_zone'], data['ip'])
            elif "delete_record" in request.args:
                delete_record(hosted_zone_id, data['name_record'], data['hosted_zone'])
            elif "update_record" in request.args:
                update_record(hosted_zone_id, data['name_record'], data['hosted_zone'], data['ip'])
            else:
                return ["The action doesn't exist", 400]  # Change: Improved error message
        else:
            # Error handling for hosted zone issues
            if hosted_zone_id == HOSTED_ZONE_NOT_FOUND:
                return ["The hosted zone name doesn't exist", 400]  # Change: Improved error message
            if hosted_zone_id == HOSTED_ZONE_NOT_OWNED:
                return ["This is not your hosted zone", 400]  # Change: Improved error message


# Change: Added comments to explain the function's purpose
def action_jenkins_route53(jenkins_info):
    """
    Jenkins pipeline handler for Route53 actions. Performs Route53 actions
    based on the input provided by the Jenkins job.

    Args:
        jenkins_info (dict): Dictionary containing information about the action to be performed.
    """
    if "create_zone" in jenkins_info['action']:
        return create_zone(jenkins_info['hosted_zone'], jenkins_info['myname'], "Jenkins")
    else:
        hosted_zone_id = get_hosted_zone_id(jenkins_info['hosted_zone'], jenkins_info['myname'], "Jenkins")
        if hosted_zone_id != HOSTED_ZONE_NOT_OWNED and hosted_zone_id != HOSTED_ZONE_NOT_FOUND:
            # Perform the respective action based on the Jenkins info
            if "list_records" in jenkins_info['action']:
                list_records(hosted_zone_id)
            elif "create_record" in jenkins_info['action']:
                create_record(hosted_zone_id, jenkins_info['name_record'], jenkins_info['hosted_zone'],
                              jenkins_info['ip'])
            elif "delete_record" in jenkins_info['action']:
                delete_record(hosted_zone_id, jenkins_info['name_record'], jenkins_info['hosted_zone'])
            elif "update_record" in jenkins_info['action']:
                update_record(hosted_zone_id, jenkins_info['name_record'], jenkins_info['hosted_zone'],
                              jenkins_info['ip'])
            else:
                return "The action doesn't exist"  # Change: Improved error message
        else:
            # Error handling for hosted zone issues
            if hosted_zone_id == HOSTED_ZONE_NOT_FOUND:
                return ["The hosted zone name doesn't exist", 400]  # Change: Improved error message
            if hosted_zone_id == HOSTED_ZONE_NOT_OWNED:
                return ["This is not your hosted zone", 400]  # Change: Improved error message


# Change: Added comments to explain the function's role
def get_hosted_zone_id(name_host_zone, myname, info):
    """
    Retrieves the hosted zone ID by name and checks if the user has the appropriate
    permissions based on a 'MyName' tag.

    Args:
        name_host_zone (str): The name of the hosted zone to retrieve.
        myname (str): The user's name to verify ownership of the hosted zone.
        info (str): Additional info to append to 'myname' for verification.

    Returns:
        str: The hosted zone ID if found and verified, or HOSTED_ZONE_NOT_OWNED if not owned, or HOSTED_ZONE_NOT_FOUND if not found.
    """
    myname = f"{myname} {info}"
    client = boto3.client('route53')
    list_hosted_zone = client.list_hosted_zones_by_name(DNSName=name_host_zone)

    # Iterate through hosted zones to find a match
    for host_zones in list_hosted_zone['HostedZones']:
        if name_host_zone + "." == host_zones['Name']:
            hosted_zone_id = host_zones['Id'].split('/')[-1]

            # Check if the hosted zone is tagged with 'MyName'
            response = client.list_tags_for_resource(ResourceType='hostedzone', ResourceId=hosted_zone_id)
            for tag in response['ResourceTagSet']['Tags']:
                if tag['Key'] == 'MyName' and tag['Value'] == myname:
                    return hosted_zone_id
            else:
                return HOSTED_ZONE_NOT_OWNED  # This is not your hosted zone
    else:
        return HOSTED_ZONE_NOT_FOUND  # The hosted zone name doesn't exist
