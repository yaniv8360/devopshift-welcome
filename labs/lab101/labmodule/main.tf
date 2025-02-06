module "ec2_vm" {
  source         = "./modules/ec2"
  ami            = "ami-0ecc0e0d5986a576d"   # Example AMI ID provided by your instructor
  instance_type  = "t2.micro"
  vm_name        = "yaniv-vm"
  # The region variable is optional since it has a default value
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