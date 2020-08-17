resource "aws_vpc" "example_machine" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags = {
    Name = "aws_example"
  }
}
resource "aws_eip" "example_machine" {
  instance = aws_instance.example_machine.id
  vpc      = true
}


