
data "aws_region" "current" {}

data "aws_caller_identity" "current" {}

locals {
  aws_region = data.aws_region.current.name
  account_id = data.aws_caller_identity.current.account_id
}

variable "enrichment_bucket" {
  type = string
}

variable "lambda_layer_arn" {
  type = string
}

variable "wc_cluster_name" {
  type = string
}

variable "wc_cluster_id" {
  type = string
}

variable "lambda_security_group_id" {
  type = string
}

variable "lambda_subnet_id" {
  type = string
}

output "notification_router_func_arn" {
  value = aws_lambda_function.cyberscan_enrichments_notification_router_func.arn
}

output "reputation_processing_input_prep_func_arn" {
  value = aws_lambda_function.cyberscan_enrichments_reputation_processing_input_prep_func.arn
}

output "vulnerability_processing_input_prep_func_arn" {
  value = aws_lambda_function.cyberscan_enrichments_vulnerability_processing_input_prep_func.arn
}

output "breach_conform_input_prep_func_arn" {
  value = aws_lambda_function.cyberscan_enrichments_breach_conform_input_prep_func.arn
}

output "breach_processing_input_prep_func_arn" {
  value = aws_lambda_function.cyberscan_enrichments_breach_processing_input_prep_func.arn
}

output "tool_processing_input_prep_func_arn" {
  value = aws_lambda_function.cyberscan_enrichments_tool_processing_input_prep_func.arn
}

output "threat_actor_processing_input_prep_func_arn" {
  value = aws_lambda_function.cyberscan_enrichments_threat_actor_processing_input_prep_func.arn
}

output "iihd_processing_input_prep_func_arn" {
  value = aws_lambda_function.cyberscan_enrichments_iihd_processing_input_prep_func.arn
}
