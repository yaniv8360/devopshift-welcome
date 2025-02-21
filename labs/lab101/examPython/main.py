#!/usr/bin/python3
import jinja2
UBUNTU = "ami-0c2b8ca1dad447f8a"
AMAZON_LINUX = "ami-0f1a6835595fb9246"
ami = None
instance_type = None
region = "us-east-1"
availability_zone = "us-east-1a"
load_balancer_name  = None
print("please select machine")
print("type 1 for ubuntu")
print("type 2 for Amazon Linux")
while True:
    user_input = input()
    if user_input == "1":
        ami = UBUNTU
        break
    elif user_input == "2":
        ami = AMAZON_LINUX
        break
    else:
        print("input is not valid you have to select 1 or 2")
print("please select machine")
print("type 1 for t3.small")
print("type 2 for t3.medium")
while True:
    user_input = input()
    if user_input == "1":
        instance_type = "t3.small"
        break
    elif user_input == "2":
        instance_type = "t3.medium"
        break
    else:
        print("input is not valid you have to select 1 or 2")
print("please type Availability Zone & Region:")
user_input = input()
if user_input == "us-east-1":
    region = "us-east-1"
else:
    print("your availability zone is not ok, i chose the deafult us-east-1")
    region = "us-east-1"
print("please type Load Balancer Name:")
load_balancer_name = input()
terraform_template = """
provider "aws" {
region = "{{ region }}"
}

resource "aws_instance" "web_server" {
ami = "{{ ami }}"
instance_type = "{{ instance_type }}"
availability_zone = "{{ availability_zone }}"
subnet_id= aws_subnet.public[0].id

tags = {
Name = "YanivRoticsAmi21"
}
}

resource "aws_lb" "application_lb" {
name = "{{ load_balancer_name }}"
internal = false
load_balancer_type = "application"
security_groups = [aws_security_group.lb_sg.id]
subnets = aws_subnet.public[*].id
}

resource "aws_security_group" "lb_sg" {
name        = "YanivRotics-lbsg21"
description = "Allow HTTP inbound traffic"

ingress {
from_port   = 80
to_port     = 80
protocol    = "tcp"
cidr_blocks = ["0.0.0.0/0"]
}
}

resource "aws_lb_listener" "http_listener" {
load_balancer_arn = aws_lb.application_lb.arn
port              = 80
protocol          = "HTTP"

default_action {
type             = "forward"
target_group_arn = aws_lb_target_group.web_target_group.arn
}
}

resource "aws_lb_target_group" "web_target_group" {
name     = "YanivRotics21-target-group"
port     = 80
protocol = "HTTP"
vpc_id   = data.aws_vpc.default.id
}

resource "aws_lb_target_group_attachment" "web_instance_attachment" {
target_group_arn = aws_lb_target_group.web_target_group.arn
target_id        = aws_instance.web_server.id
}

resource "aws_subnet" "public" {
count = 2
vpc_id = data.aws_vpc.default.id
cidr_block = cidrsubnet(data.aws_vpc.default.cidr_block, 8, count.index)
availability_zone = element(["us-east-1a", "us-east-1b"], count.index)
}

data "aws_vpc" "default" {
    default = true
}
output "instance_id" {
  value= aws_instance.web_server.id
}

output "alb_dns_name" {
  value= aws_lb.application_lb.dns_name
}

output "instance_public_ip" {
  value= aws_instance.web_server.public_ip
}
"""
context = {
"region": "us-east-1",
"ami": ami,
"instance_type": instance_type,
"availability_zone": "us-east-1a",
"load_balancer_name": load_balancer_name
}
template = jinja2.Template(terraform_template)
Terraform_content = template.render(context)
with open("main.tf", "w") as file:
    file.write(Terraform_content)


