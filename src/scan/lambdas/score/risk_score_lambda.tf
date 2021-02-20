output "lambda_cs_risk_score_lambda_arn" {
  value = aws_lambda_function.cs_risk_score.arn
}

resource "aws_lambda_function" "cs_risk_score" {
  function_name    = "ScoringFxn"
  runtime          = "java8"
  handler          = "com.netscan.risk.score.ApiGatewayProxyHandler::handleRequest"
  filename         = "${path.module}/risk_score_lambda.jar"
  source_code_hash = filebase64sha256("${path.module}/risk_score_lambda.jar")
  role             = aws_iam_role.scoring_fxn_role.arn
  timeout          = "60"
  memory_size      = 512
}

resource "aws_iam_role" "scoring_fxn_role" {
  name               = "ScoringFxnRole"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_policy" "scoring_fxn_access_policy" {
  name        = "ScoringFxnS3AccessPolicy"
  description = "Policy used by the CyberScan ScoringFxn to access S3."
  policy      = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "s3:GetObject*",
                "s3:GetBucket*",
                "s3:List*",
                "s3:DeleteObject*",
                "s3:PutObject*",
                "s3:Abort*"
            ],
            "Resource": [
                "arn:aws:s3:::${var.s3_scan_bucket_name}",
                "arn:aws:s3:::${var.s3_scan_bucket_name}/*"
            ],
            "Effect": "Allow"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "scoring_fxn_role_AWSLambdaBasicExecutionRole" {
  role       = aws_iam_role.scoring_fxn_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "scoring_fxn_role_AWSLambdaVPCAccessExecutionRole" {
  role       = aws_iam_role.scoring_fxn_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_iam_role_policy_attachment" "scoring_fxn_role_ScoringFxnS3AccessPolicy" {
  role       = aws_iam_role.scoring_fxn_role.name
  policy_arn = aws_iam_policy.scoring_fxn_access_policy.arn
}

