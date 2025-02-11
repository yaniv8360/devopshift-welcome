variable "vpc_cidr" {
  type        = string
}

variable "subnet_count" {

}

variable "instance_type" {

}

variable "associate_public_ip_address" {
 type        = bool
}

variable "subnet_cidrs" {
  type    = list(string)
  default = ["10.0.1.0/24", "10.0.3.0/24", "10.0.4.0/24"]
}