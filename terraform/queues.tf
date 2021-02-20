
resource "aws_sqs_queue" "collector_queue" {
  name = "CyberScanCollectorQueue"
  message_retention_seconds = 1209600
  redrive_policy = jsonencode({
    "deadLetterTargetArn" : aws_sqs_queue.collector_dead_letter_queue.arn
    "maxReceiveCount" : 3
  })
}

resource "aws_sqs_queue" "collector_dead_letter_queue" {
  name = "CyberScanDeadLetterQueue"
  message_retention_seconds = 1209600
}
