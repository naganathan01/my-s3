provider "aws"{
    region="us-east-1"
}

# for security group

resource "aws_security_group" "terraform-test" {
  count = var.destroy_infra ? 0 : 1
  name        = "terraform-test"
  description = "Allow TLS inbound traffic"
 

  ingress {
    description      = "TLS from VPC"
    from_port        = 0
    to_port          = 22
    protocol         = "tcp"
    cidr_blocks      =  ["0.0.0.0/0"]
    
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    
  }

  tags = {
    Name = "terraform-test"
  }
}

# for instance
resource "aws_instance" "terraform-instance"{
  count = var.destroy_infra ? 0 : 1
    ami=var.my_ami_id
    instance_type=var.my_instance_type
   
     iam_instance_profile = aws_iam_instance_profile.test_profile[0].id
    # vpc_id= "vpc-0f1a4468"
    key_name = data.aws_key_pair.example.key_name
    tags={
        Name="terraformEc2ubuntu"

    }
}   

# aws launch template
resource "aws_launch_template" "terraform-template" {
  count = var.destroy_infra ? 0 : 1
  name_prefix   = "terraform-template"
  image_id      = var.my_ami_id
  instance_type = var.my_instance_type
  vpc_security_group_ids = [aws_security_group.auto-security-group[0].id]
}
resource "aws_security_group" "auto-security-group" {
 count = var.destroy_infra ? 0 : 1
  name        = "auto-security-group"
  description = "Allow TLS inbound traffic"
  vpc_id = data.aws_vpc.vpc_data.id

  ingress {
    description      = "TLS from VPC"
    from_port        = 0
    to_port          = 22
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
   
  }

  tags = {
    Name = "allow_tls"
  }
}

resource "aws_autoscaling_group" "terraform-group" {
 count = var.destroy_infra ? 0 : 1
  name               = "terraform-autoscaling"
  desired_capacity   = 1
  max_size           = 1
  min_size           = 1
  vpc_zone_identifier = [data.aws_subnet.subnet_data.id,data.aws_subnet.subnet_data1.id]

  launch_template {
    id      = aws_launch_template.terraform-template[0].id
    version = "$Latest"
  }
}

# attaching policy
resource "aws_iam_policy_attachment" "test-attach" {
  count = var.destroy_infra ? 0 : 1
  name       = "test-attachment"
  roles      = [aws_iam_role.terraform-role[0].name]
  policy_arn = aws_iam_policy.policy[0].arn
}
# instance profile
resource "aws_iam_instance_profile" "test_profile" {
 count = var.destroy_infra ? 0 : 1
  name = "test_profile-ae"
  role = aws_iam_role.terraform-role[0].name
}




# s3 bucket uploading
# resource "aws_s3_bucket_object" "object" {
# count =  var.create_infra ? 1:0
#   bucket = "terraform-6042022"
# }
