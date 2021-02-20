# API BASE PATH
resource "aws_api_gateway_resource" "cs_cyberscan_resource" {
  parent_id   = data.aws_api_gateway_rest_api.cs_api_root.root_resource_id
  path_part   = "cyberscan"
  rest_api_id = data.aws_api_gateway_rest_api.cs_api_root.id
}

resource "aws_api_gateway_deployment" "cs_api_root_stage_qa" {
  depends_on  = [data.aws_api_gateway_rest_api.cs_api_root]
  rest_api_id = data.aws_api_gateway_rest_api.cs_api_root.id
  stage_name  = var.api_deploy_stage_name

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_authorizer" "cs_api_cognito_authorizer" {
  name            = "cyberscan_auth"
  rest_api_id     = data.aws_api_gateway_rest_api.cs_api_root.id
  type            = "COGNITO_USER_POOLS"
  provider_arns   = [aws_cognito_user_pool.cs_user_pool.arn]
}

resource "aws_cognito_user_pool" "cs_user_pool" {
  name             = "Cyberscan User Pool"
  alias_attributes = ["preferred_username"]
}

resource "aws_cognito_user_pool_domain" "cs_user_pool_domain" {
  domain       = var.cognito_user_pool_domain
  user_pool_id = aws_cognito_user_pool.cs_user_pool.id
}

resource "aws_cognito_resource_server" "cs_user_pool_resource_server" {
  identifier   = "netscan-internal"
  name         = "OAuthEndpoints"
  user_pool_id = aws_cognito_user_pool.cs_user_pool.id
  scope {
    scope_description = "Analytics Endpoints"
    scope_name        = "analytics"
  }
  scope {
    scope_description = "DQM Endpoints"
    scope_name        = "dqm"
  }
  scope {
    scope_description = "Meta-Data Endpints"
    scope_name        = "metadata"
  }
  scope {
    scope_description = "Management Endpoints"
    scope_name        = "mgmt"
  }
  scope {
    scope_description = "Status Endpoints"
    scope_name        = "status"
  }
}

resource "aws_cognito_user_pool_client" "cs_user_pool_client" {
  name                                 = "Cyberscan Admin User Client"
  user_pool_id                         = aws_cognito_user_pool.cs_user_pool.id
  generate_secret                      = true
  allowed_oauth_flows                  = ["client_credentials"]
  explicit_auth_flows                  = [
    "ALLOW_CUSTOM_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH"
  ]
  allowed_oauth_scopes                 = aws_cognito_resource_server.cs_user_pool_resource_server.scope_identifiers
  allowed_oauth_flows_user_pool_client = true
  supported_identity_providers         = ["COGNITO"]
}
