
resource "aws_sfn_state_machine" "cs_scoring_pipeline" {
  name       = "cs_scoring_pipeline"
  role_arn   = aws_iam_role.cyberscan_score_state_machine_events.arn
  definition = jsonencode(
  {
    "StartAt":"cyberscan-score-generate-input-from-scan",
    "States": {
      "cyberscan-score-generate-input-from-scan": {
        "Next": "cyberscan-score-perform-scoring",
        "Type": "Task",
        "Resource": module.lambda_score.lambda_cs_generate_input_from_scan_arn
      },
      "cyberscan-score-perform-scoring": {
        "Next": "cyberscan-score-process-scoring-result",
        "Type":"Task",
        "Resource": module.lambda_score.lambda_cs_risk_score_lambda_arn
      },
      "cyberscan-score-process-scoring-result": {
        "End": true,
        "Type": "Task",
        "Resource": module.lambda_score.lambda_cs_process_scoring_results_arn
      }
    }
  })
}

resource "aws_iam_role" "cyberscan_score_state_machine_events" {
  name               = "cyberscanscorestatemachineEventsRole"
  description        = "Allows Lambda functions to call AWS services on your behalf."
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "states.amazonaws.com",
          "events.amazonaws.com"
        ]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "cyberscan_score_state_machine_events_AWSLambdaFullAccess" {
  role       = aws_iam_role.cyberscan_score_state_machine_events.name
  policy_arn = "arn:aws:iam::aws:policy/AWSLambdaFullAccess"
}

resource "aws_iam_role_policy_attachment" "cyberscan_score_state_machine_events_AWSStepFunctionsFullAccess" {
  role       = aws_iam_role.cyberscan_score_state_machine_events.name
  policy_arn = "arn:aws:iam::aws:policy/AWSStepFunctionsFullAccess"
}
