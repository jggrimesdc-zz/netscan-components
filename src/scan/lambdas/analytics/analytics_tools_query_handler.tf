data "archive_file" "cs_tools_query" {
  type        = "zip"
  source_file = "${path.module}/analytics_tools_query_handler.py"
  output_path = ".terraform/archives/analytics_tools_query_handler.zip"
}

# /cyberscan/tools/tools
resource "aws_api_gateway_resource" "analytics_tools" {
  parent_id   = aws_api_gateway_resource.analytics.id
  path_part   = "tools"
  rest_api_id = var.rest_api_id
}

# /cyberscan/analytics/tools/query
resource "aws_api_gateway_resource" "analytics_tools_query" {
  parent_id   = aws_api_gateway_resource.analytics_tools.id
  path_part   = "query"
  rest_api_id = var.rest_api_id
}

# METHOD
resource "aws_api_gateway_method" "cs_analytics_tools_query_method" {
  authorization        = "COGNITO_USER_POOLS"
  http_method          = "GET"
  resource_id          = aws_api_gateway_resource.analytics_tools_query.id
  rest_api_id          = var.rest_api_id
  authorizer_id        = var.cognito_authorizer_id
  authorization_scopes = local.authorization_scopes
}

# INTEGRATION
resource "aws_api_gateway_integration" "cs_analytics_tools_query_integration" {
  rest_api_id             = var.rest_api_id
  resource_id             = aws_api_gateway_method.cs_analytics_tools_query_method.resource_id
  http_method             = aws_api_gateway_method.cs_analytics_tools_query_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.cs_tools_query.invoke_arn
}

resource "aws_lambda_function" "cs_tools_query" {
  function_name    = "cs_analytics_tools"
  runtime          = "python3.7"
  handler          = "analytics_tools_query_handler.lambda_handler"
  filename         = data.archive_file.cs_tools_query.output_path
  source_code_hash = data.archive_file.cs_tools_query.output_base64sha256
  role             = var.lambda_role_arn
  layers           = [var.lambda_layer_arn]
  environment {
    variables = {
      DB_SECRET_NAME = "rds/wcaasmgmt"
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
resource "aws_lambda_permission" "cs_tools_query_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cs_tools_query.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${local.aws_region}:${local.account_id}:${var.rest_api_id}/*/${aws_api_gateway_method.cs_analytics_tools_query_method.http_method}${aws_api_gateway_resource.analytics_tools_query.path}"
}
