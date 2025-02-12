# this solution dosent work
import boto3
from botocore.exceptions import ClientError

# ec2_client = boto3.client("ec2")
# response = ec2_client.describe_instances()

# try:
#     ec2_client.start_instances(InstanceIds=["id1", "id2"])
#     ec2_client.stop_instances(InstanceIds=["id1", "id2"])
#     ec2_client.terminate_instances(InstanceIds=["id1", "id2"])
# except ClientError:
#     print("No such id")


def Manage_S3_Buckets():
    s3_client = boto3.client("s3")
    response = s3_client.list_buckets()
    print("""
    interactive Manage S3 Buckets,please choose:
    1 - List Buckets
    2 - Create Bucket
    3 - Delete Bucket
    """)
    user_input = input().strip()
    match user_input:
        case "1":
            print("S3 Buckets:")
            for bucket in response["Buckets"]:
                print(f"- {bucket['Name']}")
        case "2":
            print("Enter Bucket name:")
            Bucket_name = input().strip()
            if Bucket_name in response["Buckets"]:
                print("This Bucket name is already exists")
        case "3":
            print("Thanks and have a fun day! goodbye")
            exit(0)
        case _:
            print("wrong input")


def Manage_EC2_Instances():
    print("Manage_EC2_Instances")
    pass


print("""
interactive AWS resource manager,please choose:
1 - Manage S3 Buckets
2 - Manage EC2 Instances
3 - Exit
""")
user_input = input().strip()
match user_input:
    case "1":
        Manage_S3_Buckets()
    case "2":
        Manage_EC2_Instances()
    case "3":
        print("Thanks and have a fun day! goodbye")
        exit(0)
    case _:
        print("wrong input")

# s3_client = boto3.client("s3")
# response = s3_client.list_buckets()

# print("S3 Buckets:")
# for bucket in response["Buckets"]:
#     print(f"- {bucket['Name']}")

# ec2_client = boto3.client("ec2")
# response = ec2_client.describe_instances()

# try:
#     ec2_client.start_instances(InstanceIds=["id1", "id2"])
#     ec2_client.stop_instances(InstanceIds=["id1", "id2"])
#     ec2_client.terminate_instances(InstanceIds=["id1", "id2"])
# except ClientError:
#     print("No such id")
