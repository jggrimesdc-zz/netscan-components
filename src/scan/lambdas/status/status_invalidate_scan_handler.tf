data "archive_file" "cs_scan_invalidate" {
  type        = "zip"
  source_file = "${path.module}/status_invalidate_scan_handler.py"
  output_path = ".terraform/archives/status_invalidate_scan_handler.zip"
}

# /cyberscan/status/invalidate
resource "aws_api_gateway_resource" "scan_invalidate" {
  parent_id   = aws_api_gateway_resource.status.id
  path_part   = "invalidate"
  rest_api_id = var.rest_api_id
}

# /cyberscan/status/invalidate/{scan_id}
resource "aws_api_gateway_resource" "scan_invalidate_scanid" {
  parent_id   = aws_api_gateway_resource.scan_invalidate.id
  path_part   = "{scan_id}"
  rest_api_id = var.rest_api_id
}

# POST /cyberscan/status/invalidate/{scan_id}
resource "aws_api_gateway_method" "scan_invalidate_method" {
  authorization    = "NONE"
  http_method      = "POST"
  resource_id      = aws_api_gateway_resource.scan_invalidate_scanid.id
  rest_api_id      = var.rest_api_id
  api_key_required = true
}

resource "aws_api_gateway_integration" "cs_scan_invalidate_integration" {
  rest_api_id             = var.rest_api_id
  resource_id             = aws_api_gateway_method.scan_invalidate_method.resource_id
  http_method             = aws_api_gateway_method.scan_invalidate_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.cs_scan_invalidate.invoke_arn
}

resource "aws_lambda_function" "cs_scan_invalidate" {
  function_name    = "cs_scan_invalidate"
  runtime          = "python3.7"
  handler          = "status_invalidate_scan_handler.lambda_handler"
  filename         = data.archive_file.cs_scan_invalidate.output_path
  source_code_hash = data.archive_file.cs_scan_invalidate.output_base64sha256
  role             = var.lambda_role_arn
  layers           = [var.lambda_layer_arn]
  environment {
    variables = {
      WCAAS_SERVICE_CLUSTER_ID = var.wc_cluster_id
      WCAAS_SERVICE_TENANT_ID  = var.wc_tenant_id
      CRUD_API_URL             = var.wc_crud_url
      MGMT_KEYSPACE            = var.wc_mgmt_keyspace
      STATUS_KEYSPACE          = var.wc_status_keyspace
      META_DATA_KEYSPACE      = var.wc_meta_keyspace
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

resource "aws_lambda_permission" "cs_scan_invalidate_status_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cs_scan_invalidate.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${local.aws_region}:${local.account_id}:${var.rest_api_id}/*/${aws_api_gateway_method.scan_invalidate_method.http_method}${aws_api_gateway_resource.scan_invalidate.path}"
}


resource "aws_lambda_permission" "cs_scan_invalidate_status_permission_path_param" {
  statement_id  = "AllowExecutionFromAPIGateway2"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cs_scan_invalidate.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${local.aws_region}:${local.account_id}:${var.rest_api_id}/*/${aws_api_gateway_method.scan_invalidate_method.http_method}${aws_api_gateway_resource.scan_invalidate.path}/*"
}
