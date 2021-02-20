# Used by CICD script and passed to document generation
output "api_deploy_stage_name" {
  value = var.api_deploy_stage_name
}

output "aws_region" {
  value = var.aws_region
}

output "rest_api_id" {
  value = data.aws_api_gateway_rest_api.cs_api_root.id
}

output "s3_documentation_path" {
  value = var.s3_documentation_path
}
