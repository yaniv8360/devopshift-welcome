variable "region" {
  default = "us-east-1"
}
# Create VPC only if enabled
resource "aws_vpc" "custom_vpc" {
 count = 1

 cidr_block           = "10.0.0.0/16"
 enable_dns_support   = true
 enable_dns_hostnames = true

 tags = {
   Name = "YanivRotics-vpc"
 }
}

# Create subnet inside the VPC
resource "aws_subnet" "public_subnet" {
 vpc_id            = aws_vpc.custom_vpc[0].id
 cidr_block        = "10.0.1.0/24"
 map_public_ip_on_launch = true

 tags = {
   Name = "YanivRoticsPublic-subnet"
 }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.custom_vpc[0].id

  tags = {
    Name = "YanivRotics-igw"
  }
}
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.custom_vpc[0].id

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
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_rt.id
}
resource "aws_subnet" "private_subnet" {
  vpc_id     = aws_vpc.custom_vpc[0].id
  cidr_block = "10.0.2.0/24"

  tags = {
    Name = "YanivRoticsPrivate-subnet"
  }
}
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.custom_vpc[0].id

  tags = {
    Name = "private-route-table"
  }
}

resource "aws_route_table_association" "private" {
  subnet_id      = aws_subnet.private_subnet.id
  route_table_id = aws_route_table.private.id
}

# data "aws_region" "current" {}

# output "aws_region" {
#   value = data.aws_region.current.name
# }

resource "aws_security_group" "instance_sg" {
  name        = "instance-sg"
  description = "Allow SSH and HTTP traffic"
  vpc_id      = aws_vpc.custom_vpc[0].id

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
    Name = "instance-sg"
  }
}

resource "aws_key_pair" "my_key_pair" {
  key_name   = "YanivRoticsKeyPair"  # Name of the key pair in AWS
  public_key = file("id_YanivRoticsRsa.pub")  # Path to your public key file
}

# # Output the key pair name
# output "key_pair_name" {
#   value = aws_key_pair.my_key_pair.key_name
# }

# # Output the key pair ID
# output "key_pair_id" {
#   value = aws_key_pair.my_key_pair.id
# }
resource "aws_instance" "ubuntu_instance" {
  ami                    = "ami-0e1bed4f06a3b463d"
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.public_subnet.id
  vpc_security_group_ids = [aws_security_group.instance_sg.id]
  associate_public_ip_address = true
  key_name               = "YanivRoticsKeyPair"

  tags = {
    Name = "YanivRoticsUbuntuMachine"
  }
}
output "vm_public_ip" {
  value       = aws_instance.ubuntu_instance.public_ip
  description = "Public IP address of the VM"
}
