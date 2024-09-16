import argparse
import ec2
import s3
import route53
import sys

# Create the main parser
parser = argparse.ArgumentParser(description='Peer CLI for AWS:')

# Add the subparser for resource-specific arguments
subparsers = parser.add_subparsers(dest="resource", required=True, help="Specify the AWS resource to manage (s3, ec2, or route53)")

# Create EC2 parser
ec2_parser = subparsers.add_parser("ec2", help="Manage EC2 instances")
ec2_parser.add_argument("--action", choices=["list", "create", "update", "delete"], required=True, help="Action to perform on EC2")
ec2_parser.add_argument("--myname", required=True, help="Enter your name for managing")
ec2_parser.add_argument("--name", help="The name of the EC2 instance (required for create, update, and delete)")
ec2_parser.add_argument("--instance_type", choices=["t3.nano", "t4g.nano"], help="Instance type for EC2 (recommended for create)")
ec2_parser.add_argument("--status", choices=["start", "stop"], help="Start or stop the EC2 instance (required for update)")
ec2_parser.add_argument("--ami", choices=["ubuntu", "amazon"], help="The AMI for the EC2 instance (recommended for create)")

# Create S3 parser
s3_parser = subparsers.add_parser("s3", help="Manage S3 buckets")
s3_parser.add_argument("--action", choices=["list", "create", "update", "delete"], required=True, help="Action to perform on S3")
s3_parser.add_argument("--myname", required=True, help="Enter your name for managing")
s3_parser.add_argument("--name", help="The name of the S3 bucket (required for create, update, and delete)")
s3_parser.add_argument("--public", choices=["yes", "no"], help="Whether the S3 bucket should be public (recommended for create)")
s3_parser.add_argument("--filename", help="Path of the file you want to upload")

# Create Route53 parser
route53_parser = subparsers.add_parser("route53", help="Manage Route53 DNS records")
route53_parser.add_argument("--action", choices=["create_zone", "list_records", "create_record", "delete_record", "update_record"], required=True, help="Action to perform on Route53")
route53_parser.add_argument("--myname", required=True, help="Enter your name for managing")
route53_parser.add_argument("--hosted_zone", help="Hosted zone for Route53 (required for certain actions)")
route53_parser.add_argument("--name_record", help="DNS record name (required for record actions)")
route53_parser.add_argument("--ip", help="IP address for the DNS record (required for create_record)")

# Parse the arguments
args = parser.parse_args()

# Validation logic based on actions
if args.resource == "ec2":
    if args.action == "list":
        if not args.myname:
            print("Error: --myname is required for the 'list' action.")
            sys.exit(1)
    elif args.action == "create":
        if not (args.myname and args.name):
            print("Error: --myname and --name are required for the 'create' action.")
            sys.exit(1)
        if not args.instance_type:
            print("Note: It is recommended to specify an --instance_type for EC2 creation.")
        if not args.ami:
            print("Note: It is recommended to specify an --ami for EC2 creation.")
    elif args.action == "update":
        if not (args.myname and args.name and args.status):
            print("Error: --myname, --name, and --status are required for the 'update' action.")
            sys.exit(1)
    elif args.action == "delete":
        if not (args.myname and args.name):
            print("Error: --myname and --name are required for the 'delete' action.")
            sys.exit(1)

# Validation for S3
elif args.resource == "s3":
    if args.action == "list":
        if not args.myname:
            print("Error: --myname is required for the 'list' action.")
            sys.exit(1)
    elif args.action == "create":
        if not (args.myname and args.name):
            print("Error: --myname and --name are required for the 'create' action.")
            sys.exit(1)
        if not args.public:
            print("Note: It is recommended to specify --public for S3 bucket creation.")
    elif args.action == "update":
        if not (args.myname and args.name):
            print("Error: --myname and --name are required for the 'update' action.")
            sys.exit(1)
        if not args.filename:
            print("Note: It is recommended to specify --filename for updating files.")
    elif args.action == "delete":
        if not (args.myname and args.name):
            print("Error: --myname and --name are required for the 'delete' action.")
            sys.exit(1)

# Validation for Route53
elif args.resource == "route53":
    if args.action == "list_records":
        if not args.myname:
            print("Error: --myname is required for the 'list_records' action.")
            sys.exit(1)
    elif args.action == "create_zone":
        if not (args.myname and args.hosted_zone):
            print("Error: --myname and --hosted_zone are required for the 'create_zone' action.")
            sys.exit(1)
    elif args.action == "create_record":
        if not (args.myname and args.hosted_zone and args.name_record and args.ip):
            print("Error: --myname, --hosted_zone, --name_record, and --ip are required for the 'create_record' action.")
            sys.exit(1)
    elif args.action == "delete_record":
        if not (args.myname and args.hosted_zone and args.name_record):
            print("Error: --myname, --hosted_zone, and --name_record are required for the 'delete_record' action.")
            sys.exit(1)

# Dispatch to the appropriate module based on the resource type
if args.resource == "ec2":
    ec2.action_cli(args)
elif args.resource == "s3":
    s3.action(args)
elif args.resource == "route53":
    route53.action_cli(args)
