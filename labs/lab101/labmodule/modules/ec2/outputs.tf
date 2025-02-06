output "vm_public_ip" {
  value       = aws_instance.vm.public_ip
  description = "Public IP address of the VM"
  depends_on  = [null_resource.check_public_ip]
}

output "ami_used" {
  value       = aws_instance.vm.ami
  description = "AMI used to launch the VM"
}

output "region" {
  value       = var.region
  description = "AWS region used for deployment"
}
