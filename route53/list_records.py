import boto3


# Function to list all DNS records in a given Route 53 hosted zone
def list_records(hosted_zone_id):
    # Initialize the Route 53 client
    client = boto3.client('route53')

    # Retrieve all resource record sets for the specified hosted zone
    response1 = client.list_resource_record_sets(
        HostedZoneId=hosted_zone_id
    )

    # Initialize an empty list to store the formatted record details
    list_record = []

    # Iterate over each record in the response
    for record in response1['ResourceRecordSets']:
        # Append the record's name and its associated values to the list
        list_record.append(f"{record['Name']} -> {record['ResourceRecords']}")

    # Return the list of records as a string along with a success status code
    return [str(list_record), 200]
