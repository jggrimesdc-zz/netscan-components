# BASE PATH
data "aws_region" "current" {}

data "aws_caller_identity" "current" {}

locals {
  aws_region = data.aws_region.current.name
  account_id = data.aws_caller_identity.current.account_id
}

variable "s3_lambda_role" {
  type = string
}

variable "lambda_layer_arn" {
  type = string
}

variable "lambda_security_group_id" {
  type = string
}

variable "lambda_subnet_id" {
  type = string
}

variable "s3_scan_bucket_name" {
  type = string
}

variable "wc_cluster_id" {
  type = string
}

variable "wc_tenant_id" {
  type = string
}

variable "wc_crud_url" {
  type = string
}

variable "wc_dqm_keyspace" {
  type = string
}

variable "wc_mgmt_keyspace" {
  type = string
}

variable "wc_meta_keyspace" {
  type = string
}

variable "wc_score_keyspace" {
  type = string
}

variable "wc_status_keyspace" {
  type = string
}
