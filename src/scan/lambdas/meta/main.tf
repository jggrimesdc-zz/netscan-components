# BASE PATH
# /cyberscan/scan/schedule
resource "aws_api_gateway_resource" "scan_schedule" {
  parent_id   = var.aws_api_gateway_resource_scan_id
  path_part   = "schedule"
  rest_api_id = var.rest_api_id
}

# /cyberscan/scan/schedule/{schedule_id}
resource "aws_api_gateway_resource" "scan_schedule_scheduleid" {
  parent_id   = aws_api_gateway_resource.scan_schedule.id
  path_part   = "{schedule_id}"
  rest_api_id = var.rest_api_id
}

data "aws_region" "current" {}

data "aws_caller_identity" "current" {}

output "meta_schedule_submit_scan_arn" {
  value = aws_lambda_function.meta_schedule_submit_scan.arn
}

variable "s3_lambda_role" {
  type = string
}

locals {
  aws_region = data.aws_region.current.name
  account_id = data.aws_caller_identity.current.account_id
}

variable "cyberscan_resource_id" {
  type = string
}

variable "rest_api_id" {
  type = string
}

variable "cognito_authorizer_id" {
  type = string
}

variable "lambda_role_arn" {
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

variable "wc_status_keyspace" {
  type = string
}

variable "scheduled_scans_queue_url" {
  type = string
}

variable "scheduled_scans_arn" {
  type = string
}

variable "cs_scan_submit_arn" {
  type = string
}

variable "aws_api_gateway_resource_scan_id" {
  type = string
}
