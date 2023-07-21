terraform {
  cloud {
    organization = "calsoft-t"
    hostname = "app.terraform.io"
	workspaces {
      name = "terraform-aws-cals"
    }
	
	}

  }

variable "access_key" {
    description = "AWS access key"
    default = "5"
}

variable "secret_key" {
    description = "AWS secret key"
    default = "5"
}

provider "aws" {
  region  = "us-east-1a"
  access_key = "var.access_key"
  secret_key = "var.secret_key"
}

## Amazon Linux 2023 AMI Free Tier Eligible

resource "aws_instance" "app_server" {
  ami           = "ami-06ca3ca175f37dd66"
  instance_type = "t2.micro"

  tags = {
    Name = "ExampleAppServerInstance"
  }
}
