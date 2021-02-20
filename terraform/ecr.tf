# setting up the ecr repo
resource "aws_ecr_repository" "ingest_conform_repo" {
  name                 = "ingest_conform_repo"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }

#   encryption_configuration {
#     encryption_type = "kms"
#   }
}

