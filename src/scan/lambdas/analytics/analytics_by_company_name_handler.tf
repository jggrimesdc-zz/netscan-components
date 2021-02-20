data "archive_file" "cs_analytics_companyname" {
  type        = "zip"
  source_file = "${path.module}/analytics_by_company_name_handler.py"
  output_path = ".terraform/archives/analytics_by_company_name_handler.zip"
}

# /cyberscan/analytics/companyname
resource "aws_api_gateway_resource" "analytics_companyname" {
  parent_id   = aws_api_gateway_resource.analytics.id
  path_part   = "companyname"
  rest_api_id = var.rest_api_id
}

# /cyberscan/analytics/companyname/{company_name}
resource "aws_api_gateway_resource" "analytics_companyname_companyname" {
  parent_id   = aws_api_gateway_resource.analytics_companyname.id
  path_part   = "{company_name}"
  rest_api_id = var.rest_api_id
}

# METHOD
resource "aws_api_gateway_method" "cs_analytics_companyname_method" {
  authorization        = "COGNITO_USER_POOLS"
  http_method          = "GET"
  resource_id          = aws_api_gateway_resource.analytics_companyname_companyname.id
  rest_api_id          = var.rest_api_id
  authorizer_id        = var.cognito_authorizer_id
  authorization_scopes = local.authorization_scopes
}

# INTEGRATION
resource "aws_api_gateway_integration" "cs_analytics_companyname_integration" {
  rest_api_id             = var.rest_api_id
  resource_id             = aws_api_gateway_method.cs_analytics_companyname_method.resource_id
  http_method             = aws_api_gateway_method.cs_analytics_companyname_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.cs_analytics_companyname.invoke_arn
}

resource "aws_lambda_function" "cs_analytics_companyname" {
  function_name    = "cs_analytics_companyname"
  runtime          = "python3.7"
  handler          = "analytics_by_company_name_handler.handle"
  filename         = data.archive_file.cs_analytics_companyname.output_path
  source_code_hash = data.archive_file.cs_analytics_companyname.output_base64sha256
  role             = var.lambda_role_arn
  layers           = [var.lambda_layer_arn]
  environment {
    variables = {
      WCAAS_SERVICE_CLUSTER_ID = var.wc_cluster_id
      WCAAS_SERVICE_TENANT_ID  = var.wc_tenant_id
      CRUD_API_URL             = var.wc_crud_url
      ANALYTICS_KEYSPACE       = var.wc_analytics_keyspace
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

# GRANT API GATEWAY PERMISSION TO INVOKE LAMBDA
resource "aws_lambda_permission" "cs_analytics_companyname_status_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cs_analytics_companyname.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${local.aws_region}:${local.account_id}:${var.rest_api_id}/*/${aws_api_gateway_method.cs_analytics_companyname_method.http_method}${aws_api_gateway_resource.analytics_companyname_companyname.path}"
}
