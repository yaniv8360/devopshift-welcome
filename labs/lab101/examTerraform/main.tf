# Create VPC only if enabled
resource "aws_vpc" "custom_vpc" {
 count = 1

 cidr_block           = "10.0.0.0/16"
 enable_dns_support   = true
 enable_dns_hostnames = true

 tags = {
   Name = "YanivRotics-vpc"
 }
}

# Create subnet inside the VPC
resource "aws_subnet" "public_subnet" {
 vpc_id            = aws_vpc.custom_vpc[0].id
 cidr_block        = "10.0.1.0/24"
 map_public_ip_on_launch = true

 tags = {
   Name = "YanivRoticsPublic-subnet"
 }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.custom_vpc[0].id

  tags = {
    Name = "YanivRotics-igw"
  }
}
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.custom_vpc[0].id

  # Route to direct all traffic to the Internet Gateway
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "YanivRotics-rt"
  }
}
resource "aws_route_table_association" "public_rt_assoc" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_rt.id
}
resource "aws_subnet" "private_subnet" {
  vpc_id     = aws_vpc.custom_vpc[0].id
  cidr_block = "10.0.2.0/24"

  tags = {
    Name = "YanivRoticsPrivate-subnet"
  }
}
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.custom_vpc[0].id

  tags = {
    Name = "private-route-table"
  }
}

resource "aws_route_table_association" "private" {
  subnet_id      = aws_subnet.private_subnet.id
  route_table_id = aws_route_table.private.id
}