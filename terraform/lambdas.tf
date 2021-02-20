//////////////////
// API BACK-END //
//////////////////

data "archive_file" "python_libraries" {
  type        = "zip"
  source_dir  = "../layers"
  output_path = ".terraform/archives/layers.zip"
}

# PYTHON LAYER
resource "aws_lambda_layer_version" "cs_lambda_layer" {
  filename            = data.archive_file.python_libraries.output_path
  source_code_hash    = data.archive_file.python_libraries.output_base64sha256
  layer_name          = "requirements_layer"
  compatible_runtimes = ["python3.7"]
}

module "lambda_analytics" {
  source                   = "../src/scan/lambdas/analytics"
  lambda_layer_arn         = aws_lambda_layer_version.cs_lambda_layer.arn
  lambda_role_arn          = aws_iam_role.default_lambda_role.arn
  lambda_security_group_id = data.aws_security_group.lambda_security_group.id
  lambda_subnet_id         = data.aws_subnet.selected_subnet.id
  cognito_authorizer_id    = aws_api_gateway_authorizer.cs_api_cognito_authorizer.id
  rest_api_id              = data.aws_api_gateway_rest_api.cs_api_root.id
  wc_cluster_id            = var.wc_cluster_id
  wc_tenant_id             = var.wc_tenant_id
  wc_crud_url              = var.wc_crud_url
  wc_analytics_keyspace    = local.wc_analytics_keyspace
  wc_enrichments_keyspace  = local.wc_enrichments_keyspace
  wc_user_id               = var.wc_user_id
  cyberscan_resource_id    = aws_api_gateway_resource.cs_cyberscan_resource.id
}

module "lambda_dqm" {
  source                   = "../src/scan/lambdas/dqm"
  lambda_layer_arn         = aws_lambda_layer_version.cs_lambda_layer.arn
  lambda_role_arn          = aws_iam_role.default_lambda_role.arn
  lambda_security_group_id = data.aws_security_group.lambda_security_group.id
  lambda_subnet_id         = data.aws_subnet.selected_subnet.id
  cognito_authorizer_id    = aws_api_gateway_authorizer.cs_api_cognito_authorizer.id
  rest_api_id              = data.aws_api_gateway_rest_api.cs_api_root.id
  wc_cluster_id            = var.wc_cluster_id
  wc_tenant_id             = var.wc_tenant_id
  wc_crud_url              = var.wc_crud_url
  wc_dqm_keyspace          = local.wc_dqm_keyspace
  cyberscan_resource_id    = aws_api_gateway_resource.cs_cyberscan_resource.id
}

module "lambda_enrichments" {
  source                   = "../src/scan/lambdas/enrichments"
  enrichment_bucket        = var.enrichment_bucket_name
  lambda_layer_arn         = aws_lambda_layer_version.cs_lambda_layer.arn
  lambda_security_group_id = data.aws_security_group.lambda_security_group.id
  lambda_subnet_id         = data.aws_subnet.selected_subnet.id
  wc_cluster_id            = var.wc_cluster_id
  wc_cluster_name          = var.wc_cluster_name
}

module "lambda_meta" {
  source                           = "../src/scan/lambdas/meta"
  lambda_layer_arn                 = aws_lambda_layer_version.cs_lambda_layer.arn
  lambda_role_arn                  = aws_iam_role.default_lambda_role.arn
  lambda_security_group_id         = data.aws_security_group.lambda_security_group.id
  lambda_subnet_id                 = data.aws_subnet.selected_subnet.id
  cognito_authorizer_id            = aws_api_gateway_authorizer.cs_api_cognito_authorizer.id
  rest_api_id                      = data.aws_api_gateway_rest_api.cs_api_root.id
  wc_cluster_id                    = var.wc_cluster_id
  wc_tenant_id                     = var.wc_tenant_id
  wc_crud_url                      = var.wc_crud_url
  wc_dqm_keyspace                  = local.wc_dqm_keyspace
  wc_mgmt_keyspace                 = local.wc_mgmt_keyspace
  wc_meta_keyspace                 = local.wc_meta_keyspace
  wc_status_keyspace               = local.wc_status_keyspace
  cyberscan_resource_id            = aws_api_gateway_resource.cs_cyberscan_resource.id
  s3_lambda_role                   = aws_iam_role.s3_lambda_role.arn
  scheduled_scans_queue_url        = aws_sqs_queue.scheduled_scans.id
  scheduled_scans_arn              = aws_sqs_queue.scheduled_scans.arn
  cs_scan_submit_arn               = module.lambda_scan.cs_scan_submit_arn
  aws_api_gateway_resource_scan_id = module.lambda_scan.aws_api_gateway_resource_scan_id
}

module "lambda_mgmt" {
  source                   = "../src/scan/lambdas/mgmt"
  lambda_layer_arn         = aws_lambda_layer_version.cs_lambda_layer.arn
  lambda_role_arn          = aws_iam_role.default_lambda_role.arn
  lambda_security_group_id = data.aws_security_group.lambda_security_group.id
  lambda_subnet_id         = data.aws_subnet.selected_subnet.id
  cognito_authorizer_id    = aws_api_gateway_authorizer.cs_api_cognito_authorizer.id
  rest_api_id              = data.aws_api_gateway_rest_api.cs_api_root.id
  wc_cluster_id            = var.wc_cluster_id
  wc_tenant_id             = var.wc_tenant_id
  wc_crud_url              = var.wc_crud_url
  wc_mgmt_keyspace         = local.wc_mgmt_keyspace
  cyberscan_resource_id    = aws_api_gateway_resource.cs_cyberscan_resource.id
}

module "lambda_scan" {
  source                                   = "../src/scan/lambdas/scan"
  lambda_layer_arn                         = aws_lambda_layer_version.cs_lambda_layer.arn
  lambda_role_arn                          = aws_iam_role.default_lambda_role.arn
  lambda_security_group_id                 = data.aws_security_group.lambda_security_group.id
  lambda_subnet_id                         = data.aws_subnet.selected_subnet.id
  cognito_authorizer_id                    = aws_api_gateway_authorizer.cs_api_cognito_authorizer.id
  rest_api_id                              = data.aws_api_gateway_rest_api.cs_api_root.id
  wc_cluster_id                            = var.wc_cluster_id
  wc_tenant_id                             = var.wc_tenant_id
  wc_crud_url                              = var.wc_crud_url
  s3_scan_bucket_name                      = var.bucket_name
  wc_dqm_keyspace                          = local.wc_dqm_keyspace
  wc_mgmt_keyspace                         = local.wc_mgmt_keyspace
  wc_meta_keyspace                         = local.wc_meta_keyspace
  wc_status_keyspace                       = local.wc_status_keyspace
  wc_scan_submission_queue_url             = var.wc_scan_submission_queue_url
  wc_scan_submission_dead_letter_queue_url = var.wc_scan_submission_dead_letter_queue_url
  scan_report_bucket                       = var.bucket_name
  cyberscan_resource_id                    = aws_api_gateway_resource.cs_cyberscan_resource.id
  s3_lambda_role                           = aws_iam_role.s3_lambda_role.arn
}

module "lambda_score" {
  source                   = "../src/scan/lambdas/score"
  lambda_layer_arn         = aws_lambda_layer_version.cs_lambda_layer.arn
  s3_lambda_role           = aws_iam_role.s3_lambda_role.arn
  lambda_security_group_id = data.aws_security_group.lambda_security_group.id
  lambda_subnet_id         = data.aws_subnet.selected_subnet.id
  wc_cluster_id            = var.wc_cluster_id
  wc_tenant_id             = var.wc_tenant_id
  wc_crud_url              = var.wc_crud_url
  wc_dqm_keyspace          = local.wc_dqm_keyspace
  wc_mgmt_keyspace         = local.wc_mgmt_keyspace
  wc_meta_keyspace         = local.wc_meta_keyspace
  wc_score_keyspace        = local.wc_score_keyspace
  wc_status_keyspace       = local.wc_status_keyspace
  s3_scan_bucket_name      = var.bucket_name
}

module "lambda_status" {
  source                   = "../src/scan/lambdas/status"
  lambda_layer_arn         = aws_lambda_layer_version.cs_lambda_layer.arn
  lambda_role_arn          = aws_iam_role.default_lambda_role.arn
  lambda_security_group_id = data.aws_security_group.lambda_security_group.id
  lambda_subnet_id         = data.aws_subnet.selected_subnet.id
  cognito_authorizer_id    = aws_api_gateway_authorizer.cs_api_cognito_authorizer.id
  rest_api_id              = data.aws_api_gateway_rest_api.cs_api_root.id
  wc_cluster_id            = var.wc_cluster_id
  wc_tenant_id             = var.wc_tenant_id
  wc_crud_url              = var.wc_crud_url
  wc_mgmt_keyspace         = local.wc_mgmt_keyspace
  wc_status_keyspace       = local.wc_status_keyspace
  wc_meta_keyspace         = local.wc_meta_keyspace
  cyberscan_resource_id    = aws_api_gateway_resource.cs_cyberscan_resource.id
}


resource "aws_iam_role" "s3_lambda_role" {
  name               = "CyberScan-Scan-S3Put-Handler-Role"
  description        = "Allows EC2 instances to call AWS services on your behalf."
  path               = "/"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "s3.amazonaws.com",
          "lambda.amazonaws.com",
          "events.amazonaws.com",
          "apigateway.amazonaws.com"
        ]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_policy" "cyberscan_eventdriven_lambda_policy" {
  name   = "cyberscan-eventdriven-lambda-policy"
  path   = "/"
  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "ec2:CreateNetworkInterface",
                "ec2:DescribeNetworkInterfaces",
                "ec2:DeleteNetworkInterface"
            ],
            "Resource": "*",
            "Effect": "Allow"
        },
        {
            "Action": "events:*",
            "Resource": "*",
            "Effect": "Allow"
        },
        {
            "Condition": {
                "StringLike": {
                    "iam:PassedToService": "events.amazonaws.com"
                }
            },
            "Action": "iam:PassRole",
            "Resource": "arn:aws:iam::*:role/*",
            "Effect": "Allow"
        },
        {
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
            "Resource": "arn:aws:s3:::*/*",
            "Effect": "Allow"
        },
        {
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
            "Resource": "*",
            "Effect": "Allow"
        },
        {
            "Action": [
                "xray:PutTraceSegments",
                "xray:PutTelemetryRecords"
            ],
            "Resource": "*",
            "Effect": "Allow"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "s3_lambda_role_cyberscan_eventdriven" {
  role       = aws_iam_role.s3_lambda_role.name
  policy_arn = aws_iam_policy.cyberscan_eventdriven_lambda_policy.arn
}

// -----------------------------------------------------------------------------------------------

resource "aws_iam_role" "default_lambda_role" {
  name               = "cyberscan_default_iam_role"
  description        = "Allows Lambda functions to call AWS services on your behalf."
  path               = "/"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "sqs.amazonaws.com",
          "lambda.amazonaws.com"
        ]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_policy" "lambda_default_lambda_role_execution" {
  name   = "lambda-default-lambda-role-execution"
  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
       {
          "Action": [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
          ],
          "Resource": "arn:aws:logs:*:*:*",
          "Effect": "Allow"
        },
        {
          "Action": "lambda:InvokeFunction",
          "Resource": "arn:aws:lambda:${var.aws_region}:${var.aws_account}:*",
          "Effect": "Allow"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_cloudfront_api_rewrite_execution" {
  role       = aws_iam_role.default_lambda_role.name
  policy_arn = aws_iam_policy.lambda_default_lambda_role_execution.arn
}

resource "aws_iam_role_policy_attachment" "default_lambda_role_SecretsManagerReadWrite" {
  role       = aws_iam_role.default_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/SecretsManagerReadWrite"
}

resource "aws_iam_role_policy_attachment" "default_lambda_role_AmazonSQSFullAccess" {
  role       = aws_iam_role.default_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSQSFullAccess"
}

resource "aws_iam_role_policy_attachment" "default_lambda_role_AWSXRayDaemonWriteAccess" {
  role       = aws_iam_role.default_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess"
}

resource "aws_iam_role_policy_attachment" "default_lambda_role_AWSLambdaBasicExecutionRole" {
  role       = aws_iam_role.default_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "default_lambda_role_AmazonSSMReadOnlyAccess" {
  role       = aws_iam_role.default_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMReadOnlyAccess"
}

resource "aws_iam_role_policy_attachment" "default_lambda_role_AWSLambdaVPCAccessExecutionRole" {
  role       = aws_iam_role.default_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_iam_role_policy_attachment" "default_lambda_role_ElasticLoadBalancingReadOnly" {
  role       = aws_iam_role.default_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/ElasticLoadBalancingReadOnly"
}


