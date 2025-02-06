variable "region" {
  description = "AWS region to deploy resources"
  default     = "us-east-1"
}

variable "ami" {
  description = "AMI to use for the instance"
  # No default value: must be provided when using the module
}

variable "instance_type" {
  description = "EC2 instance type"
  # No default value
}

variable "vm_name" {
  description = "Name tag for the VM"
  # No default value
}
