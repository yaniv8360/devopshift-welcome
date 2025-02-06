variable "region" {
  description = "AWS region to deploy resources"
  default     = "us-east-1"
}

variable "ami" {
  description = "AMI to use for the instance"
}

variable "instance_type" {
  description = "EC2 instance type"
}

variable "vm_name" {
  description = "Name tag for the VM"
}
