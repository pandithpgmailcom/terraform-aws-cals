terraform {
  cloud {
    organization = "calsoft-t"
    hostname = "app.terraform.io"
	workspaces {
      name = "api-calsoft"
    }
	
	}

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region  = "us-east-1"
  access_key = var.access_key
  secret_key = var.secret_key
}

## Amazon Linux 2023 AMI Free Tier Eligible

resource "aws_instance" "app_server" {
  ami           = "ami-06ca3ca175f37dd66"
  instance_type = "t2.micro"

  tags = {
    Name = "ExampleAppServerInstance"
  }
}
