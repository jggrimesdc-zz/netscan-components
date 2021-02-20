
# BASE PATH
resource "aws_api_gateway_resource" "analytics" {
  parent_id   = var.cyberscan_resource_id
  path_part   = "analytics"
  rest_api_id = var.rest_api_id
}

data "aws_region" "current" {}

data "aws_caller_identity" "current" {}

locals {
  aws_region = data.aws_region.current.name
  account_id = data.aws_caller_identity.current.account_id
  authorization_scopes = ["netscan-internal/analytics"]
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

variable "wc_user_id" {
  type    = string
}

variable "wc_crud_url" {
  type = string
}

variable "wc_analytics_keyspace" {
  type    = string
}

variable "wc_enrichments_keyspace" {
  type    = string
}
