data "archive_file" "cyberscan_enrichments_breach_processing_input_prep_func" {
  type        = "zip"
  source_file = "${path.module}/emr_breach_processing_input_preparation.py"
  output_path = ".terraform/archives/emr_breach_processing_input_preparation.zip"
}

// this script is provided to spark by the lambda
resource "aws_s3_bucket_object" "report_breach_direct_to_wcaas" {
  bucket       = var.enrichment_bucket
  key          = "scripts/report_breach_direct_to_wcaas.py"
  source       = "../src/scan/emr/report_breach_direct_to_wcaas.py"
  content_type = "text/x-python"
  etag         = filemd5("../src/scan/emr/report_breach_direct_to_wcaas.py")
}

resource "aws_lambda_function" "cyberscan_enrichments_breach_processing_input_prep_func" {
  function_name    = "cyberscan-enrichments-breach-processing-input-prep-func"
  runtime          = "python3.8"
  handler          = "emr_breach_processing_input_preparation.main"
  filename         = data.archive_file.cyberscan_enrichments_breach_processing_input_prep_func.output_path
  source_code_hash = data.archive_file.cyberscan_enrichments_breach_processing_input_prep_func.output_base64sha256
  role             = aws_iam_role.cyberscan_enrichments_breach_processing_input.arn
  timeout          = "3"
  environment {
    variables = {
      BUCKET = var.enrichment_bucket
    }
  }
  tracing_config {
    mode = "PassThrough"
  }
}

resource "aws_iam_role" "cyberscan_enrichments_breach_processing_input" {
  name               = "cyberscan-enrichments-breach-processing-input-prep-role-hm1us6e7"
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

resource "aws_iam_policy" "cyberscan_enrichments_breach_processing_input_cloudwatch" {
  name   = "AWSLambdaBasicExecutionRole-46adf255-ec5c-4190-8c0b-95d9ccb2f67a"
  path   = "/service-role/"
  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "arn:aws:logs:us-east-2:${local.account_id}:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "arn:aws:logs:us-east-2:${local.account_id}:log-group:/aws/lambda/cyberscan-enrichments-breach-processing-input-prep-func:*"
            ]
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "cyberscan_enrichments_breach_processing_input_cloudwatch" {
  role       = aws_iam_role.cyberscan_enrichments_breach_processing_input.name
  policy_arn = aws_iam_policy.cyberscan_enrichments_breach_processing_input_cloudwatch.arn
}
