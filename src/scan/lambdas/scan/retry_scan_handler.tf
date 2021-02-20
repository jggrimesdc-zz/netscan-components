data "archive_file" "cs_scan_retry" {
  type        = "zip"
  source_file = "${path.module}/retry_scan_handler.py"
  output_path = ".terraform/archives/retry_scan_handler.zip"
}

# /cyberscan/scan/retry
resource "aws_api_gateway_resource" "scan_retry" {
  parent_id   = aws_api_gateway_resource.scan.id
  path_part   = "retry"
  rest_api_id = var.rest_api_id
}

# /cyberscan/scan/retry/{scan_id}
resource "aws_api_gateway_resource" "scan_retry_scanid" {
  parent_id   = aws_api_gateway_resource.scan_retry.id
  path_part   = "{scan_id}"
  rest_api_id = var.rest_api_id
}

# POST /cyberscan/scan/retry/{scan_id}
resource "aws_api_gateway_method" "scan_retry_scanid_method" {
  authorization    = "NONE"
  http_method      = "POST"
  resource_id      = aws_api_gateway_resource.scan_retry_scanid.id
  rest_api_id      = var.rest_api_id
  api_key_required = true
}


resource "aws_api_gateway_integration" "cs_scan_retry_integration" {
  rest_api_id             = var.rest_api_id
  resource_id             = aws_api_gateway_method.scan_retry_scanid_method.resource_id
  http_method             = aws_api_gateway_method.scan_retry_scanid_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.cs_scan_retry.invoke_arn
}

resource "aws_lambda_function" "cs_scan_retry" {
  function_name    = "cs_scan_retry"
  runtime          = "python3.7"
  handler          = "retry_scan_handler.handle"
  filename         = data.archive_file.cs_scan_retry.output_path
  source_code_hash = data.archive_file.cs_scan_retry.output_base64sha256
  role             = var.lambda_role_arn
  layers           = [var.lambda_layer_arn]
  environment {
    variables = {
      WCAAS_SERVICE_CLUSTER_ID  = var.wc_cluster_id
      WCAAS_SERVICE_TENANT_ID   = var.wc_tenant_id
      CRUD_API_URL              = var.wc_crud_url
      MGMT_KEYSPACE             = var.wc_meta_keyspace
      META_DATA_KEYSPACE        = var.wc_meta_keyspace
      STATUS_KEYSPACE           = var.wc_status_keyspace
      SCAN_SUBMISSION_QUEUE_URL = var.wc_scan_submission_queue_url
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
  description = "The Lambda Function that resubmits a scan request to SQS after some unanticipated failure."
}

resource "aws_lambda_permission" "cs_scan_retry_status_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cs_scan_retry.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${local.aws_region}:${local.account_id}:${var.rest_api_id}/*/${aws_api_gateway_method.scan_retry_scanid_method.http_method}${aws_api_gateway_resource.scan_retry_scanid.path}"
}