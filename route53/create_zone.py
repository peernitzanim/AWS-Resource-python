import boto3
import datetime


def create_zone(name_hosted_zone, myname, info):
    myname = f"{myname} {info}"
    x = datetime.datetime.now()
    route53 = boto3.client('route53')
    try:
        response = route53.create_hosted_zone(
            Name=name_hosted_zone,
            VPC={
                'VPCRegion': 'us-east-1',
                'VPCId': 'vpc-01fa3051c3f32df2e'
            },
            CallerReference=str(x),
            HostedZoneConfig={'PrivateZone': True}
        )

        hosted_zone_id = response['HostedZone']['Id'].split('/')[-1]

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
        print("Create The Zone")
        return ["Create The Zone", 200]
    except Exception as e:
        if "in region us-east-1 has already been associated with the hosted " in str(e):
            return ["Cant create the hosted zone -> thr name of this zone exists", 400]
        else:
            return [str(e), 400]