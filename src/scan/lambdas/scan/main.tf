# BASE PATH
resource "aws_api_gateway_resource" "scan" {
  parent_id   = var.cyberscan_resource_id
  path_part   = "scan"
  rest_api_id = var.rest_api_id
}

data "aws_region" "current" {}

data "aws_caller_identity" "current" {}


output "cs_scan_submit_arn" {
  value = aws_lambda_function.cs_scan_submit.arn
}

output "aws_api_gateway_resource_scan_id" {
  value = aws_api_gateway_resource.scan.id
}

locals {
  aws_region = data.aws_region.current.name
  account_id = data.aws_caller_identity.current.account_id
}

variable "s3_lambda_role" {
  type = string
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

variable "wc_scan_submission_queue_url" {
  type = string
}

variable "wc_scan_submission_dead_letter_queue_url" {
  type = string
}

variable "scan_report_bucket" {
  type = string
}

variable "s3_scan_bucket_name" {
  type = string
}

resource "aws_iam_role" "s3_api_role" {
  name               = "CyberScan-Scan-S3Put-API-Role"
  description        = "Allows S3 to call AWS services on your behalf."
  path               = "/"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "lambda.amazonaws.com",
          "s3.amazonaws.com",
          "apigateway.amazonaws.com"
        ]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_policy" "s3_list_write_all" {
  name   = "s3-list-write-all"
  path   = "/"
  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:GetObjectRetention",
                "s3:GetObjectVersionTagging",
                "s3:PutObjectLegalHold",
                "s3:GetObjectLegalHold",
                "s3:ListMultipartUploadParts",
                "s3:GetObjectVersionTorrent",
                "s3:PutObject",
                "s3:GetObjectAcl",
                "s3:GetObject",
                "s3:GetObjectTorrent",
                "s3:PutObjectRetention",
                "s3:GetObjectVersionAcl",
                "s3:GetObjectTagging",
                "s3:GetObjectVersionForReplication",
                "s3:GetObjectVersion"
            ],
            "Resource": "arn:aws:s3:::*/*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "s3:CreateAccessPoint",
                "s3:GetAccessPoint",
                "s3:GetLifecycleConfiguration",
                "s3:GetBucketTagging",
                "s3:GetInventoryConfiguration",
                "s3:PutAnalyticsConfiguration",
                "s3:ListBucketVersions",
                "s3:GetBucketLogging",
                "s3:CreateBucket",
                "s3:ListBucket",
                "s3:GetAccelerateConfiguration",
                "s3:GetBucketPolicy",
                "s3:GetObjectAcl",
                "s3:GetEncryptionConfiguration",
                "s3:GetBucketObjectLockConfiguration",
                "s3:GetBucketRequestPayment",
                "s3:GetAccessPointPolicyStatus",
                "s3:GetObjectVersionAcl",
                "s3:GetMetricsConfiguration",
                "s3:HeadBucket",
                "s3:PutBucketVersioning",
                "s3:GetBucketPublicAccessBlock",
                "s3:GetBucketPolicyStatus",
                "s3:ListBucketMultipartUploads",
                "s3:GetBucketWebsite",
                "s3:ListAccessPoints",
                "s3:ListJobs",
                "s3:GetBucketVersioning",
                "s3:PutBucketCORS",
                "s3:GetBucketAcl",
                "s3:GetBucketNotification",
                "s3:GetReplicationConfiguration",
                "s3:GetObject",
                "s3:GetAccountPublicAccessBlock",
                "s3:ListAllMyBuckets",
                "s3:PutBucketRequestPayment",
                "s3:DescribeJob",
                "s3:PutBucketLogging",
                "s3:GetBucketCORS",
                "s3:GetAnalyticsConfiguration",
                "s3:CreateJob",
                "s3:GetBucketLocation",
                "s3:GetAccessPointPolicy",
                "s3:GetObjectVersion"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "s3_api_role_s3_list_write_all" {
  role       = aws_iam_role.s3_api_role.name
  policy_arn = aws_iam_policy.s3_list_write_all.arn
}
