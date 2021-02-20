data "archive_file" "cs_process_scoring_results" {
  type        = "zip"
  source_file = "${path.module}/process_scoring_result.py"
  output_path = ".terraform/archives/process_scoring_result.zip"
}

output "lambda_cs_process_scoring_results_arn" {
  value = aws_lambda_function.cs_process_scoring_results.arn
}

resource "aws_lambda_function" "cs_process_scoring_results" {
  function_name    = "cs_process_scoring_results"
  runtime          = "python3.7"
  handler          = "process_scoring_result.main"
  filename         = data.archive_file.cs_process_scoring_results.output_path
  source_code_hash = data.archive_file.cs_process_scoring_results.output_base64sha256
  role             = var.s3_lambda_role
  layers           = [var.lambda_layer_arn]
  environment {
    variables = {
      WCAAS_SERVICE_CLUSTER_ID = var.wc_cluster_id
      WCAAS_SERVICE_TENANT_ID  = var.wc_tenant_id
      CRUD_API_URL             = var.wc_crud_url
      DQM_KEYSPACE             = var.wc_dqm_keyspace
      SCORE_KEYSPACE           = var.wc_score_keyspace
      STATUS_KEYSPACE          = var.wc_status_keyspace
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
