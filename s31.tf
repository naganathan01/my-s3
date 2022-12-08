provider "aws"{
  region = "us-east-1"
}

resource "aws_s3_bucket" "b" {
  bucket = "nathan-bucket"
  acl    = "private"
  

  tags = {
    Name        = "My-bucket"
    Environment = "Dev"
  }
}




resource "aws_s3_bucket_object" "object" {
  bucket = "nathan-bucket"
  key    = "a1.html"
  source = "C:/Users/Naganathan/frdemo/a1.html"

  
  etag = filemd5("C:/Users/Naganathan/frdemo/a1.html")
}


# test pull automate from freshservice
