data "archive_file" "cs_dqm_eventlog" {
  type        = "zip"
  source_file = "${path.module}/dqm_eventlog_handler.py"
  output_path = ".terraform/archives/dqm_eventlog_handler.zip"
}

# /cyberscan/dqm/eventlog
resource "aws_api_gateway_resource" "dqm_eventlog" {
  parent_id   = aws_api_gateway_resource.dqm.id
  path_part   = "eventlog"
  rest_api_id = var.rest_api_id
}

# /cyberscan/dqm/eventlog/{event_actor}
resource "aws_api_gateway_resource" "cs_cyberscan_dqm_eventlog_actor_resource" {
  parent_id   = aws_api_gateway_resource.dqm_eventlog.id
  path_part   = "{event_actor}"
  rest_api_id = var.rest_api_id
}

# /cyberscan/dqm/eventlog/{event_actor}/{event_action}
resource "aws_api_gateway_resource" "cs_cyberscan_dqm_eventlog_actor_action_resource" {
  parent_id   = aws_api_gateway_resource.cs_cyberscan_dqm_eventlog_actor_resource.id
  path_part   = "{event_action}"
  rest_api_id = var.rest_api_id
}

# GET /cyberscan/dqm/eventlog/{event_actor}/{event_action}
resource "aws_api_gateway_method" "cs_dqm_eventlog_method" {
  authorization        = "COGNITO_USER_POOLS"
  http_method          = "GET"
  resource_id          = aws_api_gateway_resource.cs_cyberscan_dqm_eventlog_actor_action_resource.id
  rest_api_id          = var.rest_api_id
  authorizer_id        = var.cognito_authorizer_id
  authorization_scopes = local.authorization_scopes
}

resource "aws_api_gateway_integration" "cs_dqm_eventlog_integration" {
  rest_api_id             = var.rest_api_id
  resource_id             = aws_api_gateway_method.cs_dqm_eventlog_method.resource_id
  http_method             = aws_api_gateway_method.cs_dqm_eventlog_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.cs_dqm_eventlog.invoke_arn
}

resource "aws_lambda_function" "cs_dqm_eventlog" {
  function_name    = "cs_dqm_eventlog"
  runtime          = "python3.7"
  handler          = "dqm_eventlog_handler.handle"
  filename         = data.archive_file.cs_dqm_eventlog.output_path
  source_code_hash = data.archive_file.cs_dqm_eventlog.output_base64sha256
  role             = var.lambda_role_arn
  layers           = [var.lambda_layer_arn]
  environment {
    variables = {
      WCAAS_SERVICE_CLUSTER_ID = var.wc_cluster_id
      WCAAS_SERVICE_TENANT_ID  = var.wc_tenant_id
      CRUD_API_URL             = var.wc_crud_url
      DQM_KEYSPACE             = var.wc_dqm_keyspace
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

resource "aws_lambda_permission" "cs_dqm_eventlog_status_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cs_dqm_eventlog.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${local.aws_region}:${local.account_id}:${var.rest_api_id}/*/${aws_api_gateway_method.cs_dqm_eventlog_method.http_method}${aws_api_gateway_resource.cs_cyberscan_dqm_eventlog_actor_action_resource.path}"
}