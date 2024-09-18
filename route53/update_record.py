import boto3


# Function to update a DNS record in Route 53
def update_record(hosted_zone_id, name_record, name_host_zone, ip):
    # Initialize the Route 53 client
    client = boto3.client('route53')

    # Construct the full domain name for the record
    name_record_new = name_record + "." + name_host_zone

    # List all resource record sets in the specified hosted zone
    response = client.list_resource_record_sets(
        HostedZoneId=hosted_zone_id
    )

    # Iterate through the list of resource record sets
    for record in response['ResourceRecordSets']:
        # Check if the record name matches the one we want to update
        if name_record_new + "." in record['Name']:
            # If the record is found, update (UPSERT) it with the new IP address
            response = client.change_resource_record_sets(
                ChangeBatch={
                    'Changes': [
                        {
                            'Action': 'UPSERT',
                            'ResourceRecordSet': {
                                'Name': name_record_new,
                                'ResourceRecords': [
                                    {
                                        'Value': ip,  # New IP address for the record
                                    },
                                ],
                                'TTL': record['TTL'],  # Use the existing TTL value
                                'Type': 'A',  # Assuming the record is of type 'A'
                            },
                        },
                    ],
                    'Comment': 'Web Server',
                },
                HostedZoneId=hosted_zone_id,
            )
            # Return success message and status code 200
            return ["Record updated successfully", 200]

    # If no matching record is found, return an error message and status code 400
    return ["The record doesn't exist, please check your input", 400]
