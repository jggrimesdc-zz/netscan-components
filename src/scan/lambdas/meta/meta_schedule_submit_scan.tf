data "archive_file" "meta_schedule_submit_scan" {
  type        = "zip"
  source_file = "${path.module}/meta_schedule_submit_scan.py"
  output_path = ".terraform/archives/meta_schedule_submit_scan.zip"
}

resource "aws_lambda_function" "meta_schedule_submit_scan" {
  function_name    = "meta_schedule_submit_scan"
  runtime          = "python3.7"
  handler          = "meta_schedule_submit_scan.handle"
  filename         = data.archive_file.meta_schedule_submit_scan.output_path
  source_code_hash = data.archive_file.meta_schedule_submit_scan.output_base64sha256
  role             = var.lambda_role_arn
  layers           = [var.lambda_layer_arn]

  environment {
    variables = {
      WCAAS_SERVICE_CLUSTER_ID = var.wc_cluster_id
      WCAAS_SERVICE_TENANT_ID  = var.wc_tenant_id
      CRUD_API_URL             = var.wc_crud_url
      META_DATA_KEYSPACE       = var.wc_meta_keyspace
    }
  }

  vpc_config {
    security_group_ids = [var.lambda_security_group_id]
    subnet_ids         = [var.lambda_subnet_id]
  }

  tracing_config {
    mode = "Active"
  }

  memory_size = 128
  timeout     = "30"
  description = "Submits scheduled scans by listening to the ScheduledScans SQS queue."
}

resource "aws_lambda_permission" "allow_submit_from_scheduler" {
  statement_id  = "AllowExecutionFromScheduler"
  action        = "lambda:InvokeFunction"
  function_name = var.cs_scan_submit_arn
  principal     = "lambda.amazonaws.com"
  source_arn    = aws_lambda_function.meta_schedule_submit_scan.arn
}

resource "aws_lambda_event_source_mapping" "example" {
  event_source_arn = var.scheduled_scans_arn
  function_name    = aws_lambda_function.meta_schedule_submit_scan.function_name
}
