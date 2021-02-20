# filename         = data.archive_file.cs_breach_query.output_path
# source_code_hash = data.archive_file.cs_breach_query.output_base64sha256
data "archive_file" "cs_breach_query" {
  type        = "zip"
  source_file = "${path.module}/analytics_breach_query_handler.py"
  output_path = ".terraform/archives/analytics_breach_query_handler.zip"
}

# /cyberscan/analytics/breach
resource "aws_api_gateway_resource" "analytics_breach" {
  parent_id   = aws_api_gateway_resource.analytics.id
  path_part   = "breach"
  rest_api_id = var.rest_api_id
}

# /cyberscan/analytics/breach/query
resource "aws_api_gateway_resource" "analytics_breach_query" {
  parent_id   = aws_api_gateway_resource.analytics_breach.id
  path_part   = "query"
  rest_api_id = var.rest_api_id
}

# GET /cyberscan/analytics/breach/query
resource "aws_api_gateway_method" "cs_analytics_breach_query_method" {
  authorization        = "COGNITO_USER_POOLS"
  http_method          = "GET"
  resource_id          = aws_api_gateway_resource.analytics_breach_query.id
  rest_api_id          = var.rest_api_id
  authorizer_id        = var.cognito_authorizer_id
  authorization_scopes = local.authorization_scopes
}

# INTEGRATION
resource "aws_api_gateway_integration" "cs_analytics_breach_query_integration" {
  rest_api_id             = var.rest_api_id
  resource_id             = aws_api_gateway_method.cs_analytics_breach_query_method.resource_id
  http_method             = aws_api_gateway_method.cs_analytics_breach_query_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.cs_breach_query.invoke_arn
}

resource "aws_lambda_function" "cs_breach_query" {
  function_name    = "cs_analytics_breach"
  runtime          = "python3.7"
  handler          = "analytics_breach_query_handler.lambda_handler"
  filename         = data.archive_file.cs_breach_query.output_path
  source_code_hash = data.archive_file.cs_breach_query.output_base64sha256
  role             = var.lambda_role_arn
  layers           = [var.lambda_layer_arn]
  environment {
    variables = {
      CRUD_API_URL             = var.wc_crud_url
      ENRICHMENTS_KEYSPACE     = "enrichments"
      WCAAS_SERVICE_CLUSTER_ID = var.wc_cluster_id
      WCAAS_SERVICE_TENANT_ID  = var.wc_tenant_id
      WCAAS_SERVICE_USER_ID    = var.wc_user_id
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
resource "aws_lambda_permission" "cs_breach_query_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cs_breach_query.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${local.aws_region}:${local.account_id}:${var.rest_api_id}/*/${aws_api_gateway_method.cs_analytics_breach_query_method.http_method}${aws_api_gateway_resource.analytics_breach_query.path}"
}
