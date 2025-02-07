output "vpc_cidr" {
  value       = aws_vpc.custom_vpc.cidr_block
  description = "vpc_cidr"
}
output "public_subnet_count" {
  description = "public_subnet_count"
  value       = length(aws_subnet.public_subnet)
  
}
output "instance_type" {
  description = "instance_type"
  value       = aws_instance.ubuntu_instance[*].instance_type
}
output "associate_public_ip_address" {
  description = "associate_public_ip_address"
  value       = aws_instance.ubuntu_instance[*].associate_public_ip_address
}