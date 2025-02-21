
provider "aws" {
region = "us-east-1"
}

resource "aws_instance" "web_server" {
ami = "ami-0c2b8ca1dad447f8a"
instance_type = "t3.small"
availability_zone = "us-east-1a"
subnet_id= aws_subnet.public[0].id

tags = {
Name = "YanivRoticsAmi21"
}
}

resource "aws_lb" "application_lb" {
name = "YanivRoticsALB21"
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
# cidr_block = "10.0.${count.index}.0/24"
cidr_block = cidrsubnet(data.aws_vpc.default.cidr_block, 8, count.index)
availability_zone = element(["us-east-1a", "us-east-1b"], count.index)
}

data "aws_vpc" "default" {
    default = true
}
output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.web_server.id
}

output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  value       = aws_lb.application_lb.dns_name
}

output "instance_public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.web_server.public_ip
}

output "target_group_arn" {
  description = "ARN of the Target Group"
  value       = aws_lb_target_group.web_target_group.arn
}    