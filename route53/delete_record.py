import boto3


# Function to delete a DNS record in Route 53
def delete_record(hosted_zone_id, name_record, name_host_zone):
    # Initialize the Route 53 client
    client = boto3.client('route53')

    # Construct the full domain name for the record
    name_record_new = name_record + "." + name_host_zone

    # Retrieve all resource record sets for the specified hosted zone
    response1 = client.list_resource_record_sets(
        HostedZoneId=hosted_zone_id
    )

    # Iterate through the list of resource record sets
    for record in response1['ResourceRecordSets']:
        # Check if the record name matches the one we want to delete
        if record['Name'] == name_record_new + ".":
            # If the record is found, delete it
            response = client.change_resource_record_sets(
                ChangeBatch={
                    'Changes': [
                        {
                            'Action': 'DELETE',
                            'ResourceRecordSet': {
                                'Name': name_record_new,
                                'ResourceRecords': [
                                    {
                                        'Value': record['ResourceRecords'][0]['Value'],
                                        # Use the existing record's value
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
            return [f"Delete {name_record_new} succeeded", 200]

    # If no matching record is found, return a general success message
    return ["No matching record found for deletion", 404]
