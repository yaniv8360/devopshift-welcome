provider "aws" {
  region = "us-east-1"
}

module "vpc_ec2" {
  source = "./modules/vpc_ec2"
  vpc_cidr             = "10.0.0.0/16"
  instance_type        = "t2.micro"
  subnet_count  = 2
  associate_public_ip_address = true
  subnet_cidrs = ["10.0.1.0/24", "10.0.3.0/24"]
}