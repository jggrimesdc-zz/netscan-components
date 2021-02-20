/////////////////////
// SCAN SERIALIZER //
/////////////////////

data "archive_file" "cs_scan_serializer" {
  type        = "zip"
  source_file = "${path.module}/scan_serializer.py"
  output_path = ".terraform/archives/scan_serializer.zip"
}

data "aws_s3_bucket" "s3_scan_bucket" {
  bucket = var.s3_scan_bucket_name
}

resource "aws_lambda_function" "cs_scan_serializer" {
  function_name    = "cs_scan_serializer"
  runtime          = "python3.7"
  handler          = "scan_serializer.handle"
  filename         = data.archive_file.cs_scan_serializer.output_path
  source_code_hash = data.archive_file.cs_scan_serializer.output_base64sha256
  role             = var.s3_lambda_role
  layers           = [var.lambda_layer_arn]
  environment {
    variables = {
      WCAAS_SERVICE_CLUSTER_ID  = var.wc_cluster_id
      WCAAS_SERVICE_TENANT_ID   = var.wc_tenant_id
      CRUD_API_URL              = var.wc_crud_url
      META_DATA_KEYSPACE        = var.wc_meta_keyspace
      MGMT_KEYSPACE             = var.wc_mgmt_keyspace
      STATUS_KEYSPACE           = var.wc_status_keyspace
      DQM_KEYSPACE              = var.wc_dqm_keyspace
      SCAN_SUBMISSION_QUEUE_URL = var.wc_scan_submission_queue_url
    }
  }
  vpc_config {
    security_group_ids = [var.lambda_security_group_id]
    subnet_ids         = [var.lambda_subnet_id]
  }
  tracing_config {
    mode = "Active"
  }
  timeout          = "900"
  memory_size      = "256"
}

resource "aws_lambda_permission" "cs_scan_serializer_allow_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cs_scan_serializer.arn
  principal     = "s3.amazonaws.com"
  source_arn    = data.aws_s3_bucket.s3_scan_bucket.arn
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket     = data.aws_s3_bucket.s3_scan_bucket.id
  lambda_function {
    lambda_function_arn = aws_lambda_function.cs_scan_serializer.arn
    events              = ["s3:ObjectCreated:*"]
  }
  depends_on = [aws_lambda_permission.cs_scan_serializer_allow_bucket]
}


