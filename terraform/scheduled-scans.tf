resource "aws_sqs_queue" "scheduled_scans" {
  name           = "ScheduledScans"
  redrive_policy = jsonencode({
    "deadLetterTargetArn" : aws_sqs_queue.scheduled_scans_dlq.arn
    "maxReceiveCount" : 3
  })
}

resource "aws_sqs_queue" "scheduled_scans_dlq" {
  name                      = "ScheduledScansDeadLetterQueue"
  message_retention_seconds = 1209600
}

# TODO eventbridge rule.
