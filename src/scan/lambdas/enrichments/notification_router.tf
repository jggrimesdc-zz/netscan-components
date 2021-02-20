data "archive_file" "cyberscan_enrichments_notification_router" {
  type        = "zip"
  source_file = "${path.module}/notification_router.py"
  output_path = ".terraform/archives/notification_router.zip"
}

resource "aws_lambda_function" "cyberscan_enrichments_notification_router_func" {
  function_name    = "cyberscan-enrichments-notification-router-func"
  runtime          = "python3.8"
  handler          = "notification_router.main"
  filename         = data.archive_file.cyberscan_enrichments_notification_router.output_path
  source_code_hash = data.archive_file.cyberscan_enrichments_notification_router.output_base64sha256
  role             = aws_iam_role.cyberscan_enrichments_notification_router.arn
  timeout          = "65"
  layers           = [var.lambda_layer_arn] 

  tracing_config {
    mode = "PassThrough"
  }
#   vpc_config {
#     security_group_ids = [var.lambda_security_group_id]
#     subnet_ids         = [var.lambda_subnet_id]
#   }
}

// switched from 'resource' to 'data'
data "aws_s3_bucket" "bucket_for_lambda_trigger" {
  bucket = var.enrichment_bucket
}

resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cyberscan_enrichments_notification_router_func.arn
  principal     = "s3.amazonaws.com"
  source_arn    = data.aws_s3_bucket.bucket_for_lambda_trigger.arn
}

// Adding the s3 trigger
resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = data.aws_s3_bucket.bucket_for_lambda_trigger.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.cyberscan_enrichments_notification_router_func.arn 
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "conformed/"
    filter_suffix       = "_SUCCESS"
  }

  depends_on = [aws_lambda_permission.allow_bucket]
}

resource "aws_iam_role" "cyberscan_enrichments_notification_router" {
  name               = "cyberscan-enrichments-notification-router"
  path               = "/service-role/"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_policy" "cyberscan_enrichments_notification_router_cloudwatch_policy" {
  name   = "AWSLambdaBasicExecutionRole-notification-router-func"
  path   = "/service-role/"
  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "arn:aws:logs:${local.aws_region}:${local.account_id}:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "arn:aws:logs:${local.aws_region}:${local.account_id}:log-group:/aws/lambda/cyberscan-enrichments-notification-router-func:*"
            ]
        }
    ]
}
EOF
}

resource "aws_iam_policy" "cyberscan_enrichments_notification_router_put_events_policy" {
  name   = "cyberscan-enrichments-notification-router-func-put-events"
  path   = "/service-role/"
  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "events:PutEvents",
            "Resource": "*",
            "Effect": "Allow"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "cyberscan_enrichments_notification_router_cloudwatch" {
    role = aws_iam_role.cyberscan_enrichments_notification_router.name
    policy_arn = aws_iam_policy.cyberscan_enrichments_notification_router_cloudwatch_policy.arn
}

resource "aws_iam_role_policy_attachment" "cyberscan_enrichments_notification_router_put_events" {
    role = aws_iam_role.cyberscan_enrichments_notification_router.name
    policy_arn = aws_iam_policy.cyberscan_enrichments_notification_router_put_events_policy.arn 
}

resource "aws_iam_role_policy_attachment" "cyberscan_enrichments_notification_router_AWSLambdaVPCAccessExecutionRole" {
  role       = aws_iam_role.cyberscan_enrichments_notification_router.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}
