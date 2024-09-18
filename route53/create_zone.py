import boto3
import datetime


# Function to create a private hosted zone in Route 53
def create_zone(name_hosted_zone, myname, info):
    # Add additional information to the name
    myname = f"{myname} {info}"

    # Get the current timestamp for a unique caller reference
    x = datetime.datetime.now()

    # Initialize the Route 53 client
    route53 = boto3.client('route53')

    try:
        # Create a new hosted zone in the 'us-east-1' region and associate it with a VPC
        response = route53.create_hosted_zone(
            Name=name_hosted_zone,
            VPC={
                'VPCRegion': 'us-east-1',  # Specify the region
                'VPCId': 'vpc-01fa3051c3f32df2e'  # Specify the VPC ID
            },
            CallerReference=str(x),  # Use the current timestamp as a unique reference
            HostedZoneConfig={'PrivateZone': True}  # Set the zone as private
        )

        # Extract the hosted zone ID from the response
        hosted_zone_id = response['HostedZone']['Id'].split('/')[-1]

        # Add a tag to the hosted zone with the user's name
        response = route53.change_tags_for_resource(
            ResourceType='hostedzone',
            ResourceId=hosted_zone_id,
            AddTags=[
                {
                    'Key': 'MyName',
                    'Value': myname
                },
            ]
        )

        # Print success message
        print("Created the hosted zone")
        return ["Created the hosted zone successfully", 200]

    # Handle any exceptions that occur
    except Exception as e:
        # Check if the error is due to a duplicate hosted zone name
        if "in region us-east-1 has already been associated with the hosted " in str(e):
            return ["Cannot create the hosted zone -> the zone with this name already exists", 400]
        else:
            # Return the actual error message for any other exception
            return [str(e), 400]
