// GET /cyberscan/scan/report/{scan_id}
resource "aws_api_gateway_method" "cs_get_scan_report_method" {
  authorization      = "NONE"
  http_method        = "GET"
  resource_id        = aws_api_gateway_resource.cs_scan_reportscanobj_resource.id
  rest_api_id        = var.rest_api_id
  request_parameters = {
    "method.request.path.scan_id" = true
  }
  api_key_required   = true
}

resource "aws_api_gateway_integration" "cs_get_scan_report_integration" {
  rest_api_id             = var.rest_api_id
  resource_id             = aws_api_gateway_method.cs_get_scan_report_method.resource_id
  http_method             = aws_api_gateway_method.cs_get_scan_report_method.http_method
  integration_http_method = "GET"
  type                    = "AWS"
  uri                     = "arn:aws:apigateway:${local.aws_region}:s3:path/${var.scan_report_bucket}/{folder}/report/report.json"
  cache_key_parameters    = ["method.request.path.scan_id"]
  request_parameters      = {
    "integration.request.path.folder" = "method.request.path.scan_id"
  }
  credentials             = aws_iam_role.s3_api_role.arn
}

resource "aws_api_gateway_method_response" "cs_get_scan_report_response_200" {
  rest_api_id = var.rest_api_id
  resource_id = aws_api_gateway_method.cs_get_scan_report_method.resource_id
  http_method = aws_api_gateway_method.cs_get_scan_report_method.http_method
  status_code = "200"
}

resource "aws_api_gateway_method_response" "cs_get_scan_report_response_204" {
  rest_api_id = var.rest_api_id
  resource_id = aws_api_gateway_method.cs_get_scan_report_method.resource_id
  http_method = aws_api_gateway_method.cs_get_scan_report_method.http_method
  status_code = "204"
}

resource "aws_api_gateway_method_response" "cs_get_scan_report_response_400" {
  rest_api_id = var.rest_api_id
  resource_id = aws_api_gateway_method.cs_get_scan_report_method.resource_id
  http_method = aws_api_gateway_method.cs_get_scan_report_method.http_method
  status_code = "400"
}

resource "aws_api_gateway_method_response" "cs_get_scan_report_response_502" {
  rest_api_id = var.rest_api_id
  resource_id = aws_api_gateway_method.cs_get_scan_report_method.resource_id
  http_method = aws_api_gateway_method.cs_get_scan_report_method.http_method
  status_code = "502"
}

resource "aws_api_gateway_integration_response" "cs_get_scan_report_integration_response_200" {
  depends_on        = [aws_api_gateway_integration.cs_get_scan_report_integration]
  rest_api_id       = var.rest_api_id
  resource_id       = aws_api_gateway_method.cs_get_scan_report_method.resource_id
  http_method       = aws_api_gateway_method.cs_get_scan_report_method.http_method
  status_code       = aws_api_gateway_method_response.cs_get_scan_report_response_200.status_code
  selection_pattern = "2\\d{2}"
}

resource "aws_api_gateway_integration_response" "cs_get_scan_report_integration_response_404" {
  depends_on         = [aws_api_gateway_integration.cs_get_scan_report_integration]
  rest_api_id        = var.rest_api_id
  resource_id        = aws_api_gateway_method.cs_get_scan_report_method.resource_id
  http_method        = aws_api_gateway_method.cs_get_scan_report_method.http_method
  status_code        = aws_api_gateway_method_response.cs_get_scan_report_response_204.status_code
  selection_pattern  = "404"
  response_templates = {
    "application/json" = <<EOF
#set($inputRoot = $input.path('$'))
{
  "message" : "Scan is complete, but report is missing.  Did you submit any invalid domains?"
}
EOF
  }
}

resource "aws_api_gateway_integration_response" "cs_get_scan_report_integration_response_400" {
  depends_on         = [aws_api_gateway_integration.cs_get_scan_report_integration]
  rest_api_id        = var.rest_api_id
  resource_id        = aws_api_gateway_method.cs_get_scan_report_method.resource_id
  http_method        = aws_api_gateway_method.cs_get_scan_report_method.http_method
  status_code        = aws_api_gateway_method_response.cs_get_scan_report_response_400.status_code
  selection_pattern  = "400"
  response_templates = {
    "application/json" = <<EOF
#set($inputRoot = $input.path('$'))
{
  "message" : "Error encountered accessing report.  Your scan may not be complete.  Contact netscan support if this issue continues."
}
EOF
  }
}

resource "aws_api_gateway_integration_response" "cs_get_scan_report_integration_response_500" {
  depends_on        = [aws_api_gateway_integration.cs_get_scan_report_integration]
  rest_api_id       = var.rest_api_id
  resource_id       = aws_api_gateway_method.cs_get_scan_report_method.resource_id
  http_method       = aws_api_gateway_method.cs_get_scan_report_method.http_method
  status_code       = aws_api_gateway_method_response.cs_get_scan_report_response_502.status_code
  selection_pattern = "5\\d{2}"
}
