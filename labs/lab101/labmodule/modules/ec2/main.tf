provider "aws" {
  region = var.region
}

resource "aws_security_group" "sg" {
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "vm" {
  ami                    = var.ami
  instance_type          = var.instance_type
  vpc_security_group_ids = [aws_security_group.sg.id]
  associate_public_ip_address = true

  tags = {
    Name = var.vm_name
  }
}

resource "null_resource" "check_public_ip" {
  provisioner "local-exec" {
    command = <<EOT
      if [ -z "${aws_instance.vm.public_ip}" ]; then
        echo "ERROR: Public IP address was not assigned." >&2
        exit 1
      else
        echo "We got the IP! ${aws_instance.vm.public_ip}"
      fi
    EOT
  }
  depends_on = [aws_instance.vm]
}
