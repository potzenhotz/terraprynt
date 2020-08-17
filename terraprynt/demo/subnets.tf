resource "aws_subnet" "example_machine" {
  cidr_block        = "10.0.0.0/24"
  vpc_id            = aws_vpc.example_machine.id
  availability_zone = local.subnet_region
}
resource "aws_route_table" "example_machine" {
  vpc_id = aws_vpc.example_machine.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.example_machine.id
  }
  tags = {
    Name = "example_machine"
  }
}
resource "aws_route_table_association" "example_machine" {
  subnet_id      = aws_subnet.example_machine.id
  route_table_id = aws_route_table.example_machine.id
}
