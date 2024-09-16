import boto3

client = boto3.client('route53')

def create_record(hosted_zone_id,name_record,name_host_zone,ip):
#Create:
    try:
        response = client.change_resource_record_sets(
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'CREATE',
                        'ResourceRecordSet': {
                            'Name': name_record + "." + name_host_zone,
                            'ResourceRecords': [
                                {
                                    'Value': ip,
                                },
                            ],
                            'TTL': 300,
                            'Type': 'A',
                        },
                    },
                ],
                'Comment': 'Web Server',
            },
            HostedZoneId=hosted_zone_id
        )
        print(response)
        print("Create New Record")
    except Exception as e:
        exists_error = (f"Tried to create resource record set [name='{name_record}.{name_host_zone}.', type='A'"
                        f"] but it already exists")
        if exists_error in str(e):
            print(exists_error)
        else:
            print(e)
