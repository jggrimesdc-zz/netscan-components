data "archive_file" "cyberscan_enrichments_reputation_processing_input_prep_func" {
  type        = "zip"
  source_file = "${path.module}/emr_reputation_processing_input_preparation.py"
  output_path = ".terraform/archives/emr_reputation_processing_input_preparation.zip"
}

// this script is provided to spark by the lambda
resource "aws_s3_bucket_object" "emr_reputation_processor" {
  bucket       = var.enrichment_bucket
  key          = "scripts/emr_reputation_processor.py"
  source       = "../src/scan/emr/emr_reputation_processor.py"
  content_type = "text/x-python"
  etag         = filemd5("../src/scan/emr/emr_reputation_processor.py")
}

resource "aws_lambda_function" "cyberscan_enrichments_reputation_processing_input_prep_func" {
  function_name    = "cyberscan-enrichments-reputation-processing-input-prep-func"
  runtime          = "python3.8"
  handler          = "emr_reputation_processing_input_preparation.main"
  filename         = data.archive_file.cyberscan_enrichments_reputation_processing_input_prep_func.output_path
  source_code_hash = data.archive_file.cyberscan_enrichments_reputation_processing_input_prep_func.output_base64sha256
  role             = aws_iam_role.cyberscan_enrichments_reputation_processing_input.arn
  timeout          = "3"
  layers           = [var.lambda_layer_arn]
  environment {
    variables = {
      BUCKET = var.enrichment_bucket
      CLUSTER_ID   = var.wc_cluster_id
      CLUSTER_NAME = var.wc_cluster_name
    }
  }
  tracing_config {
    mode = "PassThrough"
  }
  vpc_config {
    security_group_ids = [var.lambda_security_group_id]
    subnet_ids         = [var.lambda_subnet_id]
  }
}

resource "aws_iam_role" "cyberscan_enrichments_reputation_processing_input" {
  name               = "cyberscan-enrichments-reputation-processing-input--role-aslt8f7w"
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

resource "aws_iam_policy" "cyberscan_enrichments_reputation_processing_input_cloudwatch" {
  name   = "AWSLambdaBasicExecutionRole-986c4233-24e9-4468-9442-54bd1fe1d54c"
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
                "arn:aws:logs:us-east-2:${local.account_id}:log-group:/aws/lambda/cyberscan-enrichments-reputation-processing-input-prep-func:*"
            ]
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "cyberscan_enrichments_reputation_processing_input_cloudwatch" {
  role       = aws_iam_role.cyberscan_enrichments_reputation_processing_input.name
  policy_arn = aws_iam_policy.cyberscan_enrichments_reputation_processing_input_cloudwatch.arn
}

resource "aws_iam_role_policy_attachment" "cyberscan_enrichments_reputation_processing_input_AWSLambdaVPCAccessExecutionRole" {
  role       = aws_iam_role.cyberscan_enrichments_reputation_processing_input.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_iam_role_policy_attachment" "cyberscan_enrichments_reputation_processing_input_ElasticLoadBalancingReadOnly" {
  role       = aws_iam_role.cyberscan_enrichments_reputation_processing_input.name
  policy_arn = "arn:aws:iam::aws:policy/ElasticLoadBalancingReadOnly"
}
