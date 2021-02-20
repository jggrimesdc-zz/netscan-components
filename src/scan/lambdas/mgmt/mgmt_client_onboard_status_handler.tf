data "archive_file" "cs_mgmt_client_onboard_status" {
  type        = "zip"
  source_file = "${path.module}/mgmt_client_onboard_status_handler.py"
  output_path = ".terraform/archives/mgmt_client_onboard_status_handler.zip"
}

# /cyberscan/mgmt/client/onboard/status
resource "aws_api_gateway_resource" "mgmt_client_onboard_status" {
  parent_id   = aws_api_gateway_resource.mgmt_client_onboard.id
  path_part   = "status"
  rest_api_id = var.rest_api_id
}

# GET /cyberscan/mgmt/client/onboard/status
resource "aws_api_gateway_method" "cs_mgmt_client_onboard_status_method" {
  authorization = "NONE"
  http_method   = "GET"
  resource_id   = aws_api_gateway_resource.mgmt_client_onboard_status.id
  rest_api_id   = var.rest_api_id
}

resource "aws_api_gateway_integration" "cs_mgmt_client_onboard_status_integration" {
  rest_api_id             = var.rest_api_id
  resource_id             = aws_api_gateway_method.cs_mgmt_client_onboard_status_method.resource_id
  http_method             = aws_api_gateway_method.cs_mgmt_client_onboard_status_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.cs_mgmt_client_onboard_status.invoke_arn
}

resource "aws_lambda_function" "cs_mgmt_client_onboard_status" {
  function_name    = "cs_mgmt_client_onboard_status"
  runtime          = "python3.7"
  handler          = "mgmt_client_onboard_status_handler.handle"
  filename         = data.archive_file.cs_mgmt_client_onboard_status.output_path
  source_code_hash = data.archive_file.cs_mgmt_client_onboard_status.output_base64sha256
  role             = var.lambda_role_arn
  layers           = [var.lambda_layer_arn]
  environment {
    variables = {
      WCAAS_SERVICE_CLUSTER_ID = var.wc_cluster_id
      WCAAS_SERVICE_TENANT_ID  = var.wc_tenant_id
      CRUD_API_URL             = var.wc_crud_url
      MGMT_KEYSPACE            = var.wc_mgmt_keyspace
    }
  }
  vpc_config {
    security_group_ids = [var.lambda_security_group_id]
    subnet_ids         = [var.lambda_subnet_id]
  }

  tracing_config {
    mode = "Active"
  }

  timeout     = "10"
  description = "The Lambda Function that handles status queries for onboarding requests to the CyberScan App.  Returns the status value for the user record in WCaaS."
}

resource "aws_lambda_permission" "cs_mgmt_client_onboard_status_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cs_mgmt_client_onboard_status.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${local.aws_region}:${local.account_id}:${var.rest_api_id}/*/${aws_api_gateway_method.cs_mgmt_client_onboard_status_method.http_method}${aws_api_gateway_resource.mgmt_client_onboard_status.path}"
}
