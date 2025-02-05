provider "aws" {
  region = var.region
}

variable "region" {
  default = "us-east-1"
}
data "aws_instances" "yaniv_vm" {
  filter {
    name   = "tag:Name"
    values = ["yaniv-vm"]
  }
}

# Assuming only one instance matches, output its public IP:
output "yaniv_vm_public_ip" {
  value       = data.aws_instances.yaniv_vm.ids[0] != "" ? data.aws_instance.example.public_ip : "No instance found"
  description = "The public IP address of the yaniv-vm instance."
}

# To complete this approach, you would also add a separate data block to query that single instance by its ID:
data "aws_instance" "example" {
  instance_id = data.aws_instances.yaniv_vm.ids[0]
}
