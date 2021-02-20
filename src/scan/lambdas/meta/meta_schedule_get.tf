data "archive_file" "meta_schedule_get" {
  type        = "zip"
  source_file = "${path.module}/meta_schedule_get.py"
  output_path = ".terraform/archives/meta_schedule_get.zip"
}

# GET /cyberscan/scan/schedule
resource "aws_api_gateway_method" "cs_scan_schedule_method_get" {
  authorization = "NONE"
  http_method   = "GET"
  resource_id   = aws_api_gateway_resource.scan_schedule.id
  rest_api_id   = var.rest_api_id
}

resource "aws_api_gateway_integration" "cs_scan_schedule_integration_get" {
  rest_api_id             = var.rest_api_id
  resource_id             = aws_api_gateway_method.cs_scan_schedule_method_get.resource_id
  http_method             = aws_api_gateway_method.cs_scan_schedule_method_get.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.meta_schedule_get.invoke_arn
}

# GET /cyberscan/scan/schedule/{schedule_id}
resource "aws_api_gateway_method" "cs_scan_schedule_scheduleid_method_get" {
  authorization = "NONE"
  http_method   = "GET"
  resource_id   = aws_api_gateway_resource.scan_schedule_scheduleid.id
  rest_api_id   = var.rest_api_id
}

resource "aws_api_gateway_integration" "cs_scan_schedule_scheduleid_integration_get" {
  rest_api_id             = var.rest_api_id
  resource_id             = aws_api_gateway_method.cs_scan_schedule_scheduleid_method_get.resource_id
  http_method             = aws_api_gateway_method.cs_scan_schedule_scheduleid_method_get.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.meta_schedule_get.invoke_arn
}

resource "aws_lambda_function" "meta_schedule_get" {
  function_name    = "meta_schedule_get"
  runtime          = "python3.7"
  handler          = "meta_schedule_get.handle"
  filename         = data.archive_file.meta_schedule_get.output_path
  source_code_hash = data.archive_file.meta_schedule_get.output_base64sha256
  role             = var.lambda_role_arn
  layers           = [var.lambda_layer_arn]
  environment {
    variables = {
      WCAAS_SERVICE_CLUSTER_ID  = var.wc_cluster_id
      WCAAS_SERVICE_TENANT_ID   = var.wc_tenant_id
      CRUD_API_URL              = var.wc_crud_url
      META_DATA_KEYSPACE        = var.wc_meta_keyspace
      MGMT_KEYSPACE             = var.wc_mgmt_keyspace
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
  description = "Creates scheduled scans that can recur daily, weekly, monthly or quarterly."
}

resource "aws_lambda_permission" "cs_scan_schedule_get_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.meta_schedule_get.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${local.aws_region}:${local.account_id}:${var.rest_api_id}/*/${aws_api_gateway_method.cs_scan_schedule_method_get.http_method}${aws_api_gateway_resource.scan_schedule.path}"
}


resource "aws_lambda_permission" "cs_scan_schedule_scheduleid_get_permission" {
  statement_id  = "AllowExecutionFromAPIGateway2"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.meta_schedule_get.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${local.aws_region}:${local.account_id}:${var.rest_api_id}/*/${aws_api_gateway_method.cs_scan_schedule_scheduleid_method_get.http_method}${aws_api_gateway_resource.scan_schedule_scheduleid.path}"
}
