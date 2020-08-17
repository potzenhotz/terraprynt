resource "aws_internet_gateway" "example_machine" {
  vpc_id = aws_vpc.example_machine.id

  tags = {
    Name = "example_machine"
  }
}
