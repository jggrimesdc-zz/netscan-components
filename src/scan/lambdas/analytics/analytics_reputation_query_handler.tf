data "archive_file" "cs_analytics_reputation" {
  type        = "zip"
  source_file = "${path.module}/analytics_reputation_query_handler.py"
  output_path = ".terraform/archives/analytics_reputation_query_handler.zip"
}

# /cyberscan/analytics/reputation
resource "aws_api_gateway_resource" "analytics_reputation" {
  parent_id   = aws_api_gateway_resource.analytics.id
  path_part   = "reputation"
  rest_api_id = var.rest_api_id
}

# /cyberscan/analytics/reputation/query
resource "aws_api_gateway_resource" "analytics_reputation_query" {
  parent_id   = aws_api_gateway_resource.analytics_reputation.id
  path_part   = "query"
  rest_api_id = var.rest_api_id
}

# GET /cyberscan/analytics/reputation/query
resource "aws_api_gateway_method" "cs_analytics_reputation_method" {
  authorization        = "COGNITO_USER_POOLS"
  http_method          = "GET"
  resource_id          = aws_api_gateway_resource.analytics_reputation_query.id
  rest_api_id          = var.rest_api_id
  authorizer_id        = var.cognito_authorizer_id
  authorization_scopes = local.authorization_scopes
}

resource "aws_api_gateway_integration" "cs_analytics_reputation_integration" {
  rest_api_id             = var.rest_api_id
  resource_id             = aws_api_gateway_method.cs_analytics_reputation_method.resource_id
  http_method             = aws_api_gateway_method.cs_analytics_reputation_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.cs_analytics_reputation.invoke_arn
}

resource "aws_lambda_function" "cs_analytics_reputation" {
  function_name    = "cs_analytics_reputation"
  runtime          = "python3.7"
  handler          = "analytics_reputation_query_handler.lambda_handler"
  filename         = data.archive_file.cs_analytics_reputation.output_path
  source_code_hash = data.archive_file.cs_analytics_reputation.output_base64sha256
  role             = var.lambda_role_arn
  layers           = [var.lambda_layer_arn]
  environment {
    variables = {
      WCAAS_SERVICE_CLUSTER_ID = var.wc_cluster_id
      WCAAS_SERVICE_TENANT_ID  = var.wc_tenant_id
      WCAAS_SERVICE_USER_ID    = var.wc_user_id
      CRUD_API_URL             = var.wc_crud_url
      ANALYTICS_KEYSPACE       = var.wc_analytics_keyspace
      ENRICHMENTS_KEYSPACE     = var.wc_enrichments_keyspace
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

resource "aws_lambda_permission" "cs_analytics_reputation_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cs_analytics_reputation.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${local.aws_region}:${local.account_id}:${var.rest_api_id}/*/${aws_api_gateway_method.cs_analytics_reputation_method.http_method}${aws_api_gateway_resource.analytics_reputation_query.path}"
}
