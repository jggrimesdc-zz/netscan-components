data "archive_file" "cs_scan_poll" {
  type        = "zip"
  source_file = "${path.module}/poll_scan_handler.py"
  output_path = ".terraform/archives/poll_scan_handler.zip"
}

# /cyberscan/scan/poll
resource "aws_api_gateway_resource" "scan_poll" {
  parent_id   = aws_api_gateway_resource.scan.id
  path_part   = "poll"
  rest_api_id = var.rest_api_id
}

# POST /cyberscan/scan/poll
resource "aws_api_gateway_method" "scan_poll_method" {
  authorization    = "NONE"
  http_method      = "POST"
  resource_id      = aws_api_gateway_resource.scan_poll.id
  rest_api_id      = var.rest_api_id
  api_key_required = true
}

resource "aws_api_gateway_integration" "cs_scan_poll_integration" {
  rest_api_id             = var.rest_api_id
  resource_id             = aws_api_gateway_method.scan_poll_method.resource_id
  http_method             = aws_api_gateway_method.scan_poll_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.cs_scan_poll.invoke_arn
}

resource "aws_lambda_function" "cs_scan_poll" {
  function_name    = "cs_scan_poll"
  runtime          = "python3.7"
  handler          = "poll_scan_handler.handle"
  filename         = data.archive_file.cs_scan_poll.output_path
  source_code_hash = data.archive_file.cs_scan_poll.output_base64sha256
  role             = var.lambda_role_arn
  layers           = [var.lambda_layer_arn]
  environment {
    variables = {
      WCAAS_SERVICE_CLUSTER_ID  = var.wc_cluster_id
      WCAAS_SERVICE_TENANT_ID   = var.wc_tenant_id
      CRUD_API_URL              = var.wc_crud_url
      META_DATA_KEYSPACE        = var.wc_meta_keyspace
      STATUS_KEYSPACE           = var.wc_status_keyspace
      SCAN_SUBMISSION_QUEUE_URL = var.wc_scan_submission_queue_url
      DEAD_LETTER_QUEUE_URL     = var.wc_scan_submission_dead_letter_queue_url
      RETRY_LIMIT               = 3
    }
  }
  vpc_config {
    security_group_ids = [var.lambda_security_group_id]
    subnet_ids         = [var.lambda_subnet_id]
  }

  tracing_config {
    mode = "Active"
  }
  timeout     = "30"
  description = "The Lambda Function that submits scans to the CyberScan to SQS for polling by the collector agents.  Returns the Scan ID for the submitted scan."
}

resource "aws_lambda_permission" "cs_scan_poll_status_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cs_scan_poll.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${local.aws_region}:${local.account_id}:${var.rest_api_id}/*/${aws_api_gateway_method.scan_poll_method.http_method}${aws_api_gateway_resource.scan_poll.path}"
}
