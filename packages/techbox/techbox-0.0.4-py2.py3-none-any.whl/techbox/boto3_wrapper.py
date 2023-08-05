import boto3


class Boto3Wrapper:

    def __init__(self):
        self.ec2_client = boto3.client('ec2')

    def describe_instances_from_fields(self, fields):
        instances_info = self.ec2_client.describe_instances()
        for instance_group in instances_info['Reservations']:
            for instance in instance_group['Instances']:
                for field in fields:
                    print(field, ': ', instance[field])

    def describe_instances_basic(self):
        fields = ['ImageId', 'InstanceType', 'InstanceId',
                  'PublicDnsName', 'PrivateDnsName', 'Tags']
        self.describe_instances_from_fields(fields=fields)
