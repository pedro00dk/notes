terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "4.2.0"
    }
  }
}

variable "aws_access_key" {
  type = string
}
variable "aws_secret_key" {
  type = string
}

variable "aws_region" {
  type = string
  description = "The region where the resource will be created"
#   default = "us-east-1a"
}


provider "aws" {
    region = "us-east-1"
    access_key = var.aws_access_key
    secret_key = var.aws_secret_key
}


resource "aws_vpc" "vpc-production" {
    cidr_block = "10.0.0.0/16"
    tags = {
        Name = "vpc-production"
    }
}

resource "aws_internet_gateway" "gateway-production" {
    vpc_id = aws_vpc.vpc-production.id
}

resource "aws_route_table" "route_table-production" {
  vpc_id     = aws_vpc.vpc-production.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gateway-production.id
  }

  route {
    ipv6_cidr_block        = "::/0"
    gateway_id = aws_internet_gateway.gateway-production.id
  }

  tags = {
    Name = "route_table-production"
  }
}

resource "aws_subnet" "subnet-production-1" {
  vpc_id     = aws_vpc.vpc-production.id
  cidr_block = "10.0.1.0/24"
  availability_zone = var.aws_region

  tags = {
    Name = "subnet-production-1"
  }
}

resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.subnet-production-1.id
  route_table_id = aws_route_table.route_table-production.id
}

resource "aws_security_group" "allow-ssh-http-https" {
  name        = "allow-ssh-http-https"
  description = "Allow web trafic"
  vpc_id      = aws_vpc.vpc-production.id

  ingress {
    description      = "SSH"
    from_port        = 22
    to_port          = 22
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }
  ingress {
    description      = "HTTP"
    from_port        = 80
    to_port          = 80
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }
  ingress {
    description      = "HTTPS"
    from_port        = 443
    to_port          = 443
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }
  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "allow-ssh-http-https"
  }
}

resource "aws_network_interface" "web-server-nic" {
  subnet_id       = aws_subnet.subnet-production-1.id
  private_ips     = ["10.0.1.50"]
  security_groups = [aws_security_group.allow-ssh-http-https.id]

#   attachment {
#     instance     = aws_instance.test.id
#     device_index = 1
#   }
}

resource "aws_eip" "one" {
  vpc      = true
  network_interface = aws_network_interface.web-server-nic.id
  associate_with_private_ip = "10.0.1.50"
  depends_on = [aws_internet_gateway.gateway-production]
}


resource "aws_instance" "my-first-server" {
  ami           = "ami-04505e74c0741db8d"
  instance_type = "t2.micro"
  availability_zone = var.aws_region
  key_name = "access-key"

  network_interface {
    device_index = 0
    network_interface_id = aws_network_interface.web-server-nic.id
  }

  tags = {
      Name = "ubuntu"
  }

  user_data = <<-EOF
    #!/bin/bash
    sudo apt update --yes
    sudo apt install apache2 --yes
    sudo systemctl start apache2
    echo 'my server created using terraform' | sudo tee /var/www/html/index.html
    EOF
}

output "elastic-ip" {
    value=aws_eip.one.public_ip
}
output "server-private-ip" {
    value=aws_instance.my-first-server.private_ip
}
output "server-id" {
    value=aws_instance.my-first-server.id
}
