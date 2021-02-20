data "archive_file" "meta_schedule_delete" {
  type        = "zip"
  source_file = "${path.module}/meta_schedule_delete.py"
  output_path = ".terraform/archives/meta_schedule_delete.zip"
}

# DELETE /cyberscan/scan/schedule
resource "aws_api_gateway_method" "cs_scan_schedule_method_delete" {
  authorization = "NONE"
  http_method   = "DELETE"
  resource_id   = aws_api_gateway_resource.scan_schedule_scheduleid.id
  rest_api_id   = var.rest_api_id
}

resource "aws_api_gateway_integration" "cs_scan_schedule_integration_delete" {
  rest_api_id             = var.rest_api_id
  resource_id             = aws_api_gateway_method.cs_scan_schedule_method_delete.resource_id
  http_method             = aws_api_gateway_method.cs_scan_schedule_method_delete.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.meta_schedule_delete.invoke_arn
}

resource "aws_lambda_function" "meta_schedule_delete" {
  function_name    = "meta_schedule_delete"
  runtime          = "python3.7"
  handler          = "meta_schedule_delete.handle"
  filename         = data.archive_file.meta_schedule_delete.output_path
  source_code_hash = data.archive_file.meta_schedule_delete.output_base64sha256
  role             = var.lambda_role_arn
  layers           = [var.lambda_layer_arn]
  environment {
    variables = {
      WCAAS_SERVICE_CLUSTER_ID  = var.wc_cluster_id
      WCAAS_SERVICE_TENANT_ID   = var.wc_tenant_id
      CRUD_API_URL              = var.wc_crud_url
      MGMT_KEYSPACE             = var.wc_mgmt_keyspace
      META_DATA_KEYSPACE        = var.wc_meta_keyspace
      STATUS_KEYSPACE           = var.wc_status_keyspace
    }
  }
  vpc_config {
    security_group_ids = [var.lambda_security_group_id]
    subnet_ids         = [var.lambda_subnet_id]
  }

  tracing_config {
    mode = "Active"
  }
  timeout     = "30"
  description = "Deletes scheduled scans."
}

resource "aws_lambda_permission" "cs_scan_schedule_delete_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.meta_schedule_delete.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${local.aws_region}:${local.account_id}:${var.rest_api_id}/*/${aws_api_gateway_method.cs_scan_schedule_method_delete.http_method}${aws_api_gateway_resource.scan_schedule_scheduleid.path}"
}
