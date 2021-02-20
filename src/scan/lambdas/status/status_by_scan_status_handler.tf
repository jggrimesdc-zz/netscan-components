data "archive_file" "cs_status_status" {
  type        = "zip"
  source_file = "${path.module}/status_by_scan_status_handler.py"
  output_path = ".terraform/archives/status_by_scan_status_handler.zip"
}

# /cyberscan/status/status
resource "aws_api_gateway_resource" "cs_status_status_resource" {
  parent_id   = aws_api_gateway_resource.status.id
  path_part   = "status"
  rest_api_id = var.rest_api_id
}

# /cyberscan/status/status/{status}
resource "aws_api_gateway_resource" "cs_status_statusobj_resource" {
  parent_id   = aws_api_gateway_resource.cs_status_status_resource.id
  path_part   = "{status}"
  rest_api_id = var.rest_api_id
}

# GET /cyberscan/status/status/{status}
resource "aws_api_gateway_method" "cs_status_status_method" {
  authorization = "NONE"
  http_method   = "GET"
  resource_id   = aws_api_gateway_resource.cs_status_statusobj_resource.id
  rest_api_id   = var.rest_api_id
}

resource "aws_api_gateway_integration" "cs_status_status_integration" {
  rest_api_id             = var.rest_api_id
  resource_id             = aws_api_gateway_method.cs_status_status_method.resource_id
  http_method             = aws_api_gateway_method.cs_status_status_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.cs_status_status.invoke_arn
}

resource "aws_lambda_function" "cs_status_status" {
  function_name    = "cs_status_status"
  runtime          = "python3.7"
  handler          = "status_by_scan_status_handler.handle"
  filename         = data.archive_file.cs_status_status.output_path
  source_code_hash = data.archive_file.cs_status_status.output_base64sha256
  role             = var.lambda_role_arn
  layers           = [var.lambda_layer_arn]
  environment {
    variables = {
      WCAAS_SERVICE_CLUSTER_ID = var.wc_cluster_id
      WCAAS_SERVICE_TENANT_ID  = var.wc_tenant_id
      CRUD_API_URL             = var.wc_crud_url
      MGMT_KEYSPACE            = var.wc_mgmt_keyspace
      STATUS_KEYSPACE          = var.wc_status_keyspace
    }
  }
  vpc_config {
    security_group_ids = [var.lambda_security_group_id]
    subnet_ids         = [var.lambda_subnet_id]
  }
  tracing_config {
    mode = "Active"
  }
  timeout          = "30"
}

resource "aws_lambda_permission" "cs_status_status_status_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cs_status_status.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${local.aws_region}:${local.account_id}:${var.rest_api_id}/*/${aws_api_gateway_method.cs_status_status_method.http_method}${aws_api_gateway_resource.cs_status_statusobj_resource.path}"
}