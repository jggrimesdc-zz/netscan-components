data "archive_file" "cs_analytics_domain" {
  type        = "zip"
  source_file = "${path.module}/analytics_by_domain_handler.py"
  output_path = ".terraform/archives/analytics_by_domain_handler.zip"
}

# cyberscan/analytics/domain
resource "aws_api_gateway_resource" "analytics_domain" {
  parent_id   = aws_api_gateway_resource.analytics.id
  path_part   = "domain"
  rest_api_id = var.rest_api_id
}

# cyberscan/analytics/domain/{domain}
resource "aws_api_gateway_resource" "analytics_domain_domain" {
  parent_id   = aws_api_gateway_resource.analytics_domain.id
  path_part   = "{domain}"
  rest_api_id = var.rest_api_id
}

# GET cyberscan/analytics/domain/{domain}
resource "aws_api_gateway_method" "cs_analytics_domain_method" {
  authorization        = "COGNITO_USER_POOLS"
  http_method          = "GET"
  resource_id          = aws_api_gateway_resource.analytics_domain_domain.id
  rest_api_id          = var.rest_api_id
  authorizer_id        = var.cognito_authorizer_id
  authorization_scopes = local.authorization_scopes
}

# INTEGRATION
resource "aws_api_gateway_integration" "cs_analytics_domain_integration" {
  rest_api_id             = var.rest_api_id
  resource_id             = aws_api_gateway_method.cs_analytics_domain_method.resource_id
  http_method             = aws_api_gateway_method.cs_analytics_domain_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.cs_analytics_domain.invoke_arn
}

resource "aws_lambda_function" "cs_analytics_domain" {
  function_name    = "cs_analytics_domain"
  runtime          = "python3.7"
  handler          = "analytics_by_domain_handler.handle"
  filename         = data.archive_file.cs_analytics_domain.output_path
  source_code_hash = data.archive_file.cs_analytics_domain.output_base64sha256
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
resource "aws_lambda_permission" "cs_analytics_domain_status_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cs_analytics_domain.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${local.aws_region}:${local.account_id}:${var.rest_api_id}/*/${aws_api_gateway_method.cs_analytics_domain_method.http_method}${aws_api_gateway_resource.analytics_domain_domain.path}"
}
