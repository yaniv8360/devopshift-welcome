import boto3
import json
from botocore.exceptions import ClientError
instance_id = "i-0d3275960b1528267"
ec2_client = boto3.client('ec2', region_name="us-east-1")
response = ec2_client.describe_instances(InstanceIds=[instance_id])
state_of_the_instance = response['Reservations'][0]['Instances'][0]['State']['Name']
print(f"the state:{state_of_the_instance}")
if state_of_the_instance != "running":
    print("state of the instance is not running")
    exit()
instance = response['Reservations'][0]['Instances'][0]
public_ip = instance.get('PublicIpAddress')
print(f"public ip is:{public_ip}")
elb_client = boto3.client('elbv2')
alb_name = "YanivRoticsALB21"
response = elb_client.describe_load_balancers(Names=[alb_name])
state = response['LoadBalancers'][0]['State']
print(f"ths state of ALB is:{state}")
ALB_dns_name = response['LoadBalancers'][0]['DNSName']
print(f"ths dns name of ALB is:{ALB_dns_name}")
dict_to_jsonFile = {
    "instance_id": instance_id,
    "instance_state": state_of_the_instance,
    "public_ip": public_ip,
    "load_balancer_dns": ALB_dns_name
}
with open("aws_validation.json", "w") as f:
    json.dump(dict_to_jsonFile, f)
