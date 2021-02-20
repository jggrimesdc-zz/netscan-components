data "archive_file" "cs_mgmt_client_onboard" {
  type        = "zip"
  source_file = "${path.module}/mgmt_client_onboard_handler.py"
  output_path = ".terraform/archives/mgmt_client_onboard_handler.zip"
}

# /cyberscan/mgmt/client
resource "aws_api_gateway_resource" "mgmt_client" {
  parent_id   = aws_api_gateway_resource.mgmt.id
  path_part   = "client"
  rest_api_id = var.rest_api_id
}

# /cyberscan/mgmt/client/onboard
resource "aws_api_gateway_resource" "mgmt_client_onboard" {
  parent_id   = aws_api_gateway_resource.mgmt_client.id
  path_part   = "onboard"
  rest_api_id = var.rest_api_id
}

# POST cyberscan/mgmt/client/onboard
resource "aws_api_gateway_method" "cs_mgmt_client_onboard_method" {
  authorization = "NONE"
  http_method   = "POST"
  resource_id   = aws_api_gateway_resource.mgmt_client_onboard.id
  rest_api_id   = var.rest_api_id
}

resource "aws_api_gateway_integration" "cs_mgmt_client_onboard_integration" {
  rest_api_id             = var.rest_api_id
  resource_id             = aws_api_gateway_method.cs_mgmt_client_onboard_method.resource_id
  http_method             = aws_api_gateway_method.cs_mgmt_client_onboard_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.cs_mgmt_client_onboard.invoke_arn
}

resource "aws_lambda_function" "cs_mgmt_client_onboard" {
  function_name    = "cs_mgmt_client_onboard"
  runtime          = "python3.7"
  handler          = "mgmt_client_onboard_handler.handle"
  filename         = data.archive_file.cs_mgmt_client_onboard.output_path
  source_code_hash = data.archive_file.cs_mgmt_client_onboard.output_base64sha256
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
  timeout          = "10"
  description      = "The Lambda Function that handles onboarding requests to the CyberScan App.  Onboards a user if they don't exist in WCaaS, returns existing user's information, or fails when given invalid headers."
}

resource "aws_lambda_permission" "cs_mgmt_client_onboard_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cs_mgmt_client_onboard.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${local.aws_region}:${local.account_id}:${var.rest_api_id}/*/${aws_api_gateway_method.cs_mgmt_client_onboard_method.http_method}${aws_api_gateway_resource.mgmt_client_onboard.path}"
}
