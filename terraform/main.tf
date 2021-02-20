provider "aws" {
  version = "~> 2.51"
  region = var.aws_region

  # sanity check -- only allows terraform to interact with
  # the aws account id that is provided by the variables
  allowed_account_ids = [var.aws_account]

}

terraform {
  backend "s3" {

  }
}

# Assertions
locals {
  assert_region_matches = var.aws_region != local.aws_region ? file("ERROR: mismatch between specified region (${var.aws_region}) and actual region (${local.aws_region})") : null
}

//////////////////////////////
// STATIC NETWORKING ASSETS //
//////////////////////////////
data "aws_vpc" "selected_vpc" {
  id = var.vpc_id
}

data "aws_subnet" "selected_subnet" {
  id = var.subnet_id
}

data "aws_security_group" "lambda_security_group" {
  id = var.lambda_sg_id
}

////////////////////
// STATIC  ASSETS //
////////////////////

data "aws_api_gateway_rest_api" "cs_api_root" {
  name = "cyberscan-api-root"
}
