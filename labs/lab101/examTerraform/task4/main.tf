provider "aws" {
  region = "us-east-1"  # choose your desired region
}
resource "aws_vpc" "custom_vpc" {

 cidr_block           = "10.0.0.0/16"
 enable_dns_support   = true
 enable_dns_hostnames = true

 tags = {
   Name = "YanivRotics-vpc"
 }
}
# Get available availability zones
data "aws_availability_zones" "available" {
  state = "available"
}
# Create two public subnets in different AZs
resource "aws_subnet" "public" {
  count                   = 3
  vpc_id                  = aws_vpc.custom_vpc.id
  cidr_block              = cidrsubnet(aws_vpc.custom_vpc.cidr_block, 8, count.index)
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true
}
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.custom_vpc.id

  tags = {
    Name = "YanivRotics-igw"
  }
}
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.custom_vpc.id

  # Route to direct all traffic to the Internet Gateway
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "YanivRotics-rt"
  }
}
resource "aws_route_table_association" "public_rt_assoc" {
  count          = 3
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public_rt.id
}
# Security Group for the Load Balancer
resource "aws_security_group" "lb_sg" {
  name   = "YanivRotics-lbsg"
  vpc_id = aws_vpc.custom_vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
resource "aws_security_group" "instance_sg" {
  name        = "YanivRotics-sg07"
  description = "Allow SSH and HTTP traffic"
  vpc_id      = aws_vpc.custom_vpc.id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "YanivRotics-sg07"
  }
}
# Create the ALB
resource "aws_lb" "app_lb" {
  name               = "YanivRoticsAppLb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.lb_sg.id]
  subnets            = aws_subnet.public[*].id
}
# Create the Target Group for the ALB
resource "aws_lb_target_group" "app_tg" {
  name     = "YavniRoticsAppTg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.custom_vpc.id

  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    interval            = 30
    protocol            = "HTTP"
    path                = "/"  # health check endpoint
  }
}
# Create a Listener on the ALB to forward traffic to the Target Group
resource "aws_lb_listener" "app_listener" {
  load_balancer_arn = aws_lb.app_lb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app_tg.arn
  }
}
# Create a Launch Template for EC2 instances
resource "aws_launch_template" "app_lt" {
  name_prefix   = "YanivRoticsApp-"
  image_id      = "ami-0e1bed4f06a3b463d"
  instance_type = "t2.micro"

  # Associate the instance security group
  network_interfaces {
    associate_public_ip_address = true
    security_groups             = [aws_security_group.instance_sg.id]
  }

  user_data = base64encode(<<-EOF
    #!/bin/bash
    yum update -y
    yum install -y httpd
    systemctl start httpd
    echo "<html><body><h1>Hello from EC2</h1></body></html>" > /var/www/html/index.html
  EOF
  )
}
resource "aws_autoscaling_group" "app_asg" {
  name                      = "YanivRoticsApp-asg"
  max_size                  = 3
  min_size                  = 1
  desired_capacity          = 1
  vpc_zone_identifier       = aws_subnet.public[*].id  # Places instances in the public subnets

  launch_template {
    id      = aws_launch_template.app_lt.id
    version = "$Latest"
  }

  # Associate the instances with the target group so they receive ALB traffic
  target_group_arns = [aws_lb_target_group.app_tg.arn]
  
  health_check_type         = "EC2"
  health_check_grace_period = 300

  tag {
    key                 = "Name"
    value               = "app-instance"
    propagate_at_launch = true
  }
}
output "alb_dns_name" {
  value       = aws_lb.app_lb.dns_name
  description = "The DNS name of the Application Load Balancer"
}

