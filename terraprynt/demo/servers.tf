resource "aws_instance" "example_machine" {
  ami                    = local.ami_id
  instance_type          = "t2.micro"
  vpc_security_group_ids = ["${aws_security_group.example_machine.id}"]
  tags = {
    Name = "aws_example"
  }
  subnet_id = aws_subnet.example_machine.id
}
