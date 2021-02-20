resource "aws_iam_role" "cyberscan_enrichments_execution" {
  name               = "StepFunctions-cyberscan-enrichments-state-machine-role-3e3bba78"
  path               = "/service-role/"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "states.amazonaws.com"
      },
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_policy" "stepfn_emr_create_cluster" {
  name        = "ElasticMapReduceRunJobFlowManagementScopedAccessPolicy-ec605aef-0167-4830-85e4-12b010db0bca"
  description = "Allows AWS Step Functions to create a cluster on your behalf."
  path        = "/service-role/"
  policy      = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "elasticmapreduce:RunJobFlow",
                "elasticmapreduce:DescribeCluster",
                "elasticmapreduce:TerminateJobFlows"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "iam:PassRole",
            "Resource": [
                "arn:aws:iam::${var.aws_account}:role/EMR_EC2_DefaultRole",
                "${aws_iam_role.cyberscan_enrichments_emr_role.arn}"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "events:PutTargets",
                "events:PutRule",
                "events:DescribeRule"
            ],
            "Resource": [
                "arn:aws:events:${var.aws_region}:${var.aws_account}:rule/StepFunctionsGetEventForEMRRunJobFlowRule"
            ]
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "stepfn_emr_create_cluster" {
  role       = aws_iam_role.cyberscan_enrichments_execution.name
  policy_arn = aws_iam_policy.stepfn_emr_create_cluster.arn
}

resource "aws_iam_policy" "stepfn_xray" {
  name        = "XRayAccessPolicy-bbd8e5c6-0150-44ed-bf6b-6d85f8cd4982"
  description = "Allow AWS Step Functions to call X-Ray daemon on your behalf"
  path        = "/service-role/"
  policy      = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "xray:PutTraceSegments",
                "xray:PutTelemetryRecords",
                "xray:GetSamplingRules",
                "xray:GetSamplingTargets"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "stepfn_xray" {
  role       = aws_iam_role.cyberscan_enrichments_execution.name
  policy_arn = aws_iam_policy.stepfn_xray.arn
}

resource "aws_iam_policy" "stepfn_lambda" {
  name        = "LambdaInvokeScopedAccessPolicy-0a03e5ad-c0d1-42a9-aaf1-27e0528c557d"
  description = "Allow AWS Step Functions to invoke Lambda functions on your behalf"
  path        = "/service-role/"
  policy      = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction"
            ],
            "Resource": [
                "${module.lambda_enrichments.notification_router_func_arn}",
                "${module.lambda_enrichments.vulnerability_processing_input_prep_func_arn}",
                "${module.lambda_enrichments.reputation_processing_input_prep_func_arn}",
                "${module.lambda_enrichments.breach_conform_input_prep_func_arn}",
                "${module.lambda_enrichments.breach_processing_input_prep_func_arn}",
                "${module.lambda_enrichments.tool_processing_input_prep_func_arn}",
                "${module.lambda_enrichments.threat_actor_processing_input_prep_func_arn}",
                "${module.lambda_enrichments.iihd_processing_input_prep_func_arn}"
            ]
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "stepfn_lambda" {
  role       = aws_iam_role.cyberscan_enrichments_execution.name
  policy_arn = aws_iam_policy.stepfn_lambda.arn
}

resource "aws_iam_policy" "stepfn_emr_add_step" {
  name        = "ElasticMapReduceAddJobFlowStepsManagementFullAccess-db420a1e-9b75-457e-9517-1bb1fa64fe76"
  description = "Allows AWS Step Functions to add a step to a cluster on your behalf."
  path        = "/service-role/"
  policy      = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "elasticmapreduce:AddJobFlowSteps",
                "elasticmapreduce:DescribeStep",
                "elasticmapreduce:CancelSteps"
            ],
            "Resource": "arn:aws:elasticmapreduce:*:*:cluster/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "events:PutTargets",
                "events:PutRule",
                "events:DescribeRule"
            ],
            "Resource": [
                "arn:aws:events:${var.aws_region}:${var.aws_account}:rule/StepFunctionsGetEventForEMRAddJobFlowStepsRule"
            ]
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "stepfn_emr_add_step" {
  role       = aws_iam_role.cyberscan_enrichments_execution.name
  policy_arn = aws_iam_policy.stepfn_emr_add_step.arn
}

resource "aws_iam_policy" "stepfn_emr_terminate_cluster" {
  name        = "ElasticMapReduceTerminateJobFlowsManagementFullAccessPolicy-ef5f5413-8413-4cb1-9862-a725bce48c47"
  description = "Allows AWS Step Functions to terminate a cluster on your behalf."
  path        = "/service-role/"
  policy      = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "elasticmapreduce:TerminateJobFlows",
                "elasticmapreduce:DescribeCluster"
            ],
            "Resource": "arn:aws:elasticmapreduce:*:*:cluster/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "events:PutTargets",
                "events:PutRule",
                "events:DescribeRule"
            ],
            "Resource": [
                "arn:aws:events:${var.aws_region}:${var.aws_account}:rule/StepFunctionsGetEventForEMRTerminateJobFlowsRule"
            ]
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "stepfn_emr_terminate_cluster" {
  role       = aws_iam_role.cyberscan_enrichments_execution.name
  policy_arn = aws_iam_policy.stepfn_emr_terminate_cluster.arn
}

// --------------------------------------------------------------------------------------------------------------------

resource "aws_iam_role" "cyberscan_enrichments_emr_role" {
  name               = "cyberscan-enrichments-emr-role"
  description        = "Allows Elastic MapReduce to call AWS services such as EC2 on your behalf."
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "elasticmapreduce.amazonaws.com"
      },
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "cyberscan_enrichments_emr_role_AmazonElasticMapReduceRole" {
  role       = aws_iam_role.cyberscan_enrichments_emr_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceRole"
}

resource "aws_iam_role_policy_attachment" "cyberscan_enrichments_emr_role_AmazonElasticMapReduceforAutoScalingRole" {
  role       = aws_iam_role.cyberscan_enrichments_emr_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceforAutoScalingRole"
}

// --------------------------------------------------------------------------------------------------------------------
