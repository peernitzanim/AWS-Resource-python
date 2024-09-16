import boto3


def update_record(hosted_zone_id, name_record, name_host_zone, ip):
    client = boto3.client('route53')
    name_record_new = name_record + "." + name_host_zone
    response = client.list_resource_record_sets(
        HostedZoneId=hosted_zone_id
    )
    for record in response['ResourceRecordSets']:
        if name_record_new + "." in record['Name']:
            response = client.change_resource_record_sets(
                ChangeBatch={
                    'Changes': [
                        {
                            'Action': 'UPSERT',
                            'ResourceRecordSet': {
                                'Name': name_record_new,
                                'ResourceRecords': [
                                    {
                                        'Value': ip,
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
            print("update the record")
            return "update the record"
    else:
        print("The record doesnt exists check yourself")
        return ["The record doesnt exists check yourself", 400]
