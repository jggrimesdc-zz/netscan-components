# /cyberscan/scan/report
resource "aws_api_gateway_resource" "cs_scan_report_resource" {
  parent_id   = aws_api_gateway_resource.scan.id
  path_part   = "report"
  rest_api_id = var.rest_api_id
}

# /cyberscan/scan/report/{scan_id}
resource "aws_api_gateway_resource" "cs_scan_reportscanobj_resource" {
  parent_id   = aws_api_gateway_resource.cs_scan_report_resource.id
  path_part   = "{scan_id}"
  rest_api_id = var.rest_api_id
}

# /cyberscan/scan/report/{scan_id}/{file_name}
resource "aws_api_gateway_resource" "cs_scan_reportscanobjfilename_resource" {
  parent_id   = aws_api_gateway_resource.cs_scan_reportscanobj_resource.id
  path_part   = "{file_name}"
  rest_api_id = var.rest_api_id
}

# POST /cyberscan/scan/report/{scan_id}/{file_name}
resource "aws_api_gateway_method" "cs_scan_report_method" {
  authorization      = "NONE"
  http_method        = "POST"
  resource_id        = aws_api_gateway_resource.cs_scan_reportscanobjfilename_resource.id
  rest_api_id        = var.rest_api_id
  request_parameters = {
    "method.request.path.scan_id"   = true
    "method.request.path.file_name" = true
  }
  api_key_required   = true
}

resource "aws_api_gateway_integration" "cs_scan_report_integration" {
  rest_api_id             = var.rest_api_id
  resource_id             = aws_api_gateway_method.cs_scan_report_method.resource_id
  http_method             = aws_api_gateway_method.cs_scan_report_method.http_method
  integration_http_method = "PUT"
  type                    = "AWS"
  uri                     = "arn:aws:apigateway:${local.aws_region}:s3:path/${var.scan_report_bucket}/{folder}/{file}"
  cache_key_parameters    = [
    "method.request.path.scan_id",
    "method.request.path.file_name"
  ]
  request_parameters      = {
    "integration.request.path.folder" = "method.request.path.scan_id"
    "integration.request.path.file"   = "method.request.path.file_name"
  }
  credentials             = aws_iam_role.s3_api_role.arn
}

resource "aws_api_gateway_method_response" "cs_scan_report_response_200" {
  rest_api_id = var.rest_api_id
  resource_id = aws_api_gateway_resource.cs_scan_reportscanobjfilename_resource.id
  http_method = aws_api_gateway_method.cs_scan_report_method.http_method
  status_code = "200"
}

resource "aws_api_gateway_method_response" "cs_scan_report_response_400" {
  rest_api_id = var.rest_api_id
  resource_id = aws_api_gateway_resource.cs_scan_reportscanobjfilename_resource.id
  http_method = aws_api_gateway_method.cs_scan_report_method.http_method
  status_code = "400"
}

resource "aws_api_gateway_method_response" "cs_scan_report_response_502" {
  rest_api_id = var.rest_api_id
  resource_id = aws_api_gateway_resource.cs_scan_reportscanobjfilename_resource.id
  http_method = aws_api_gateway_method.cs_scan_report_method.http_method
  status_code = "502"
}

resource "aws_api_gateway_integration_response" "cs_scan_report_integration_response_200" {
  depends_on        = [aws_api_gateway_integration.cs_scan_report_integration]
  rest_api_id       = var.rest_api_id
  resource_id       = aws_api_gateway_resource.cs_scan_reportscanobjfilename_resource.id
  http_method       = aws_api_gateway_method.cs_scan_report_method.http_method
  status_code       = aws_api_gateway_method_response.cs_scan_report_response_200.status_code
  selection_pattern = "2\\d{2}"
}

resource "aws_api_gateway_integration_response" "cs_scan_report_integration_response_400" {
  depends_on        = [aws_api_gateway_integration.cs_scan_report_integration]
  rest_api_id       = var.rest_api_id
  resource_id       = aws_api_gateway_resource.cs_scan_reportscanobjfilename_resource.id
  http_method       = aws_api_gateway_method.cs_scan_report_method.http_method
  status_code       = aws_api_gateway_method_response.cs_scan_report_response_400.status_code
  selection_pattern = "4\\d{2}"
}

resource "aws_api_gateway_integration_response" "cs_scan_report_integration_response_500" {
  depends_on        = [aws_api_gateway_integration.cs_scan_report_integration]
  rest_api_id       = var.rest_api_id
  resource_id       = aws_api_gateway_resource.cs_scan_reportscanobjfilename_resource.id
  http_method       = aws_api_gateway_method.cs_scan_report_method.http_method
  status_code       = aws_api_gateway_method_response.cs_scan_report_response_502.status_code
  selection_pattern = "5\\d{2}"
}
