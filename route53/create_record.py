import boto3

# Initialize the Route 53 client
client = boto3.client('route53')


# Function to create a new DNS record in a Route 53 hosted zone
def create_record(hosted_zone_id, name_record, name_host_zone, ip):
    try:
        # Create a new A record for the specified name and IP address
        response = client.change_resource_record_sets(
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'CREATE',  # Specify the action to create a new record
                        'ResourceRecordSet': {
                            'Name': name_record + "." + name_host_zone,  # Full domain name
                            'ResourceRecords': [
                                {
                                    'Value': ip,  # IP address for the A record
                                },
                            ],
                            'TTL': 300,  # Set Time-to-Live for the record
                            'Type': 'A',  # Record type 'A' (IPv4 address)
                        },
                    },
                ],
                'Comment': 'Web Server',  # Optional comment for the record change
            },
            HostedZoneId=hosted_zone_id  # Hosted zone where the record will be created
        )
        # Return success message and HTTP status code
        return ["Record created successfully", 200]

    # Handle exceptions that occur during record creation
    except Exception as e:
        # Check if the error is due to an existing record with the same name and type
        exists_error = (f"Tried to create resource record set [name='{name_record}.{name_host_zone}.', type='A' "
                        f"] but it already exists")
        if exists_error in str(e):
            return [exists_error, 400]
        else:
            # Return the actual error message for any other exception
            return [str(e), 400]
