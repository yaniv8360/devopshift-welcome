module "ec2_vm" {
  source         = "./modules/ec2"
  ami            = "ami-0ecc0e0d5986a576d"
  instance_type  = "t2.micro"
  vm_name        = "yaniv-vm"
}

output "machine_public_ip" {
  value       = module.ec2_vm.vm_public_ip
  description = "Public IP address of the machine"
}

output "machine_ami" {
  value       = module.ec2_vm.ami_used
  description = "AMI used for the machine"
}

output "aws_region" {
  value       = module.ec2_vm.region
  description = "AWS region used for deployment"
}