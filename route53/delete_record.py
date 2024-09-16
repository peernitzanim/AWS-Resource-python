import boto3


def delete_record(hosted_zone_id,name_record, name_host_zone):
    client = boto3.client('route53')
    name_record_new = name_record + "." + name_host_zone
    response1 = client.list_resource_record_sets(
        HostedZoneId=hosted_zone_id
    )
    for record in response1['ResourceRecordSets']:
        if record['Name'] == name_record_new + ".":
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
                                    },
                                ],
                                'TTL': record['TTL'],
                                'Type': 'A',
                            },
                        },
                    ],
                    'Comment': 'Web Server',
                },
                HostedZoneId=hosted_zone_id,
            )
            print(f"Delete {name_record_new} success")
            return f"Delete {name_record_new} success"
    print("Success")
    return "success"