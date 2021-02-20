data "archive_file" "cs_scan_submit" {
  type        = "zip"
  source_file = "${path.module}/submit_scan_handler.py"
  output_path = ".terraform/archives/submit_scan_handler.zip"
}

# /cyberscan/scan/submit
resource "aws_api_gateway_resource" "scan_submit" {
  parent_id   = aws_api_gateway_resource.scan.id
  path_part   = "submit"
  rest_api_id = var.rest_api_id
}

# POST /cyberscan/scan/submit
resource "aws_api_gateway_method" "cs_scan_submit_method" {
  authorization = "NONE"
  http_method   = "POST"
  resource_id   = aws_api_gateway_resource.scan_submit.id
  rest_api_id   = var.rest_api_id
}

resource "aws_api_gateway_integration" "cs_scan_submit_integration" {
  rest_api_id             = var.rest_api_id
  resource_id             = aws_api_gateway_method.cs_scan_submit_method.resource_id
  http_method             = aws_api_gateway_method.cs_scan_submit_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.cs_scan_submit.invoke_arn
}

resource "aws_lambda_function" "cs_scan_submit" {
  function_name    = "cs_scan_submit"
  runtime          = "python3.7"
  handler          = "submit_scan_handler.handle"
  filename         = data.archive_file.cs_scan_submit.output_path
  source_code_hash = data.archive_file.cs_scan_submit.output_base64sha256
  role             = var.lambda_role_arn
  layers           = [var.lambda_layer_arn]
  environment {
    variables = {
      WCAAS_SERVICE_CLUSTER_ID  = var.wc_cluster_id
      WCAAS_SERVICE_TENANT_ID   = var.wc_tenant_id
      CRUD_API_URL              = var.wc_crud_url
      MGMT_KEYSPACE             = var.wc_mgmt_keyspace
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
  description = "The Lambda Function that submits scans to the CyberScan to SQS for polling by the collector agents.  Returns the Scan ID for the submitted scan."
}

resource "aws_lambda_permission" "cs_scan_submit_status_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cs_scan_submit.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${local.aws_region}:${local.account_id}:${var.rest_api_id}/*/${aws_api_gateway_method.cs_scan_submit_method.http_method}${aws_api_gateway_resource.scan_submit.path}"
}
