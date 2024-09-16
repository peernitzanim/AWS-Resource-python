import boto3


def list_records(hosted_zone_id):
    client = boto3.client('route53')
    response1 = client.list_resource_record_sets(
        HostedZoneId=hosted_zone_id
    )
    list_record = []
    for record in response1['ResourceRecordSets']:
        list_record.append(f"{record['Name']} -> {record['ResourceRecords']}")
    print(list_record)

