data "archive_file" "meta_schedule_querier" {
  type        = "zip"
  source_file = "${path.module}/meta_schedule_querier.py"
  output_path = ".terraform/archives/meta_schedule_querier.zip"
}

resource "aws_lambda_function" "meta_schedule_querier" {
  function_name    = "meta_schedule_querier"
  runtime          = "python3.7"
  handler          = "meta_schedule_querier.handle"
  filename         = data.archive_file.meta_schedule_querier.output_path
  source_code_hash = data.archive_file.meta_schedule_querier.output_base64sha256
  role             = var.lambda_role_arn
  layers           = [var.lambda_layer_arn]

  environment {
    variables = {
      WCAAS_SERVICE_CLUSTER_ID  = var.wc_cluster_id
      WCAAS_SERVICE_TENANT_ID   = var.wc_tenant_id
      CRUD_API_URL              = var.wc_crud_url
      META_DATA_KEYSPACE        = var.wc_meta_keyspace
      SCHEDULED_SCANS_QUEUE_URL = var.scheduled_scans_queue_url
    }
  }

  vpc_config {
    security_group_ids = [var.lambda_security_group_id]
    subnet_ids         = [var.lambda_subnet_id]
  }

  tracing_config {
    mode = "Active"
  }
  memory_size = 256
  timeout     = "30"
  description = "Runs scans for a specific recurrence - daily, weekly, monthly or quarterly."
}

resource "aws_sqs_queue_policy" "scheduled_scans_policy" {
  queue_url = var.scheduled_scans_queue_url
  policy    = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "SQS:SendMessage",
      "Resource": "${var.scheduled_scans_arn}",
      "Condition": {
        "ArnEquals": {
          "aws:SourceArn": "${aws_lambda_function.meta_schedule_querier.arn}"
        }
      }
    }
  ]
}

EOF
}
