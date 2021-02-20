data "aws_region" "current" {}

locals {
  # same as var.aws_region (they could match)
  aws_region              = data.aws_region.current.name
  wc_mgmt_keyspace        = "mgmt"
  wc_meta_keyspace        = "meta"
  wc_status_keyspace      = "status"
  wc_analytics_keyspace   = "analytics"
  wc_enrichments_keyspace = "enrichments"
  wc_dqm_keyspace         = "dqm"
  wc_score_keyspace       = "score"
  lambdas_zip_base_path   = "../src/scan/lambdas"
}

variable "aws_account" {
  type        = string
  description = "AWS Account ID"
}

variable "aws_region" {
  type        = string
  description = "AWS Region"
}

variable "vpc_id" {
  type        = string
  description = "VPC ID (vpc-xxx...)"
}

variable "subnet_id" {
  type        = string
  description = "Subnet ID (subnet-xxx...)"
}

variable "lambda_sg_id" {
  type        = string
  description = "Security Group ID for Lambdas (sg-xxx...)"
}

variable "bucket_name" {
  type        = string
  description = "Scan Report S3 Bucket"
}

variable "enrichment_bucket_name" {
  type        = string
  description = "Enrichment S3 Bucket"
}

variable "cognito_user_pool_domain" {
  type        = string
  description = "Cognito User Pool Domain"
}

variable "api_deploy_stage_name" {
  type        = string
  description = "Environment name for API Deploy Stage"
}

variable "wc_cluster_name" {
  type        = string
  description = "WCAAS Cluster Name"
}

variable "wc_cluster_id" {
  type        = string
  description = "Wide Column Cluster ID"
}

variable "wc_tenant_id" {
  type        = string
  description = "Wide Column Tenant ID"
}

variable "wc_crud_url" {
  type        = string
  description = "Wide Column Crud URL"
}

variable "wc_scan_submission_queue_url" {
  type        = string
  description = "SQS URL for Scan Submission"
}

variable "wc_scan_submission_dead_letter_queue_url" {
  type        = string
  description = "DLQ URL for Scan Submission"
}

variable "wc_user_id" {
  type = string
}

variable "s3_documentation_path" {
  type        = string
  description = "S3 Path to output the generated OpenApi documentation"
}
