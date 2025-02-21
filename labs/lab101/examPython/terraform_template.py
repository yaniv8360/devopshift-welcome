# Map user inputs to jinja2 template variables

ami = ami_options.get(ami_choice, "ami-?????")
instance_type = instance_types.get(instance_type_choice, "t3.small")

terraform_template = """
provider "aws" {
 region = "{{ region }}"
}

resource "aws_instance" "web_server" {
 ami = "{{ ami }}"
 instance_type = "{{ instance_type }}"
 availability_zone = "{{ availability_zone }}"

 tags = {
   Name = "WebServer"
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
 name        = "lb_security_group"
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
 name     = "web-target-group"
 port     = 80
 protocol = "HTTP"
 vpc_id   = aws_vpc.main.id
}

resource "aws_lb_target_group_attachment" "web_instance_attachment" {
 target_group_arn = aws_lb_target_group.web_target_group.arn
 target_id        = aws_instance.web_server.id
}

resource "aws_subnet" "public" {
 count = 2
 vpc_id = aws_vpc.main.id
 cidr_block = "10.0.${count.index}.0/24"
 availability_zone = element(["us-east-1a", "us-east-1b"], count.index)
}

resource "aws_vpc" "main" {
 cidr_block = "10.0.0.0/16"
}
"""