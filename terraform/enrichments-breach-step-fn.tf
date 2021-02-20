resource "aws_sfn_state_machine" "cyberscan_enrichments_breach" {
  name       = "cyberscan-enrichments-breach"
  role_arn   = aws_iam_role.cyberscan_enrichments_execution.arn
  definition = jsonencode(
  {
    "StartAt": "cyberscan-enrichments-breach-which-size",
    "States": {
      "cyberscan-enrichments-breach-which-size": {
        "Type": "Choice",
        "Choices": [
          {
            Variable: "$.detail.s3.object.size",
            NumericLessThan: 10000000000,
            Next: "cyberscan-enrichments-breach-small-cluster-creation"
          },
          {
            Variable: "$.detail.enrichment_type",
            NumericGreaterThanEquals: 10000000000,
            Next: "cyberscan-enrichments-breach-large-cluster-creation"
          }
        ]
      },
      "cyberscan-enrichments-breach-small-cluster-creation": {
        "Next": "cyberscan-enrichments-breach-conform-input-prep",
        "Type": "Task",
        "ResultPath": "$.detail.emr",
        "Resource": "arn:aws:states:::elasticmapreduce:createCluster.sync",
        "Parameters": {
          "Instances": {
            "Ec2SubnetIds": [
              var.subnet_id
            ],
            "InstanceCount": 5,
            "KeepJobFlowAliveWhenNoSteps": true,
            "MasterInstanceType": "m5.xlarge",
            "SlaveInstanceType": "m5.xlarge"
          },
          "JobFlowRole": "EMR_EC2_DefaultRole",
          "Name": "cyberscan-enrichments-breach-cluster",
          "ServiceRole": aws_iam_role.cyberscan_enrichments_emr_role.name,
          "Applications": [
            {
              Name: "spark"
            }
          ],
          "AutoScalingRole": aws_iam_role.cyberscan_enrichments_emr_role.name,
          "BootstrapActions": [
            {
              Name: "Custom Action",
              ScriptBootstrapAction: {
                "Path": "s3://${aws_s3_bucket_object.cluster_bootstrap.bucket}/${aws_s3_bucket_object.cluster_bootstrap.key}"
              }
            }
          ],
          "ReleaseLabel": "emr-5.30.1",
          "VisibleToAllUsers": true
        }
      },
      "cyberscan-enrichments-breach-large-cluster-creation": {
        "Next": "cyberscan-enrichments-breach-conform-input-prep",
        "Type": "Task",
        "ResultPath": "$.detail.emr",
        "Resource": "arn:aws:states:::elasticmapreduce:createCluster.sync",
        "Parameters": {
          "Instances": {
            "Ec2SubnetIds": [
              var.subnet_id
            ],
            "InstanceCount": 7,
            "KeepJobFlowAliveWhenNoSteps": true,
            "MasterInstanceType": "m5.xlarge",
            "SlaveInstanceType": "m5.xlarge"
          },
          "JobFlowRole": "EMR_EC2_DefaultRole",
          "Name": "cyberscan-enrichments-breach-cluster",
          "ServiceRole": aws_iam_role.cyberscan_enrichments_emr_role.name,
          "Applications": [
            {
              Name: "spark"
            }
          ],
          "AutoScalingRole": aws_iam_role.cyberscan_enrichments_emr_role.name,
          "BootstrapActions": [
            {
              Name: "Custom Action",
              ScriptBootstrapAction: {
                "Path": "s3://${aws_s3_bucket_object.cluster_bootstrap.bucket}/${aws_s3_bucket_object.cluster_bootstrap.key}"
              }
            }
          ],
          "ReleaseLabel": "emr-5.30.1",
          "VisibleToAllUsers": true
        }
      },
      "cyberscan-enrichments-breach-conform-input-prep": {
        "Next": "cyberscan-enrichments-breach-add-conform-step",
        "Type": "Task",
        "Resource": module.lambda_enrichments.breach_conform_input_prep_func_arn
      },
      "cyberscan-enrichments-breach-add-conform-step": {
        "Next": "cyberscan-enrichments-breach-processing-input-prep",
        "Type": "Task",
        "ResultPath": null,
        "Resource": "arn:aws:states:::elasticmapreduce:addStep.sync",
        "Parameters": {
          "ClusterId.$": "$.detail.emr.ClusterId",
          "Step": {
            "Name": "cyberscan-enrichments-breach-conform-step",
            "ActionOnFailure": "TERMINATE_CLUSTER",
            "HadoopJarStep": {
              "Jar": "command-runner.jar",
              "Args.$": "$.detail.sparkargs"
            }
          }
        }
      },
      "cyberscan-enrichments-breach-processing-input-prep": {
        "Next": "cyberscan-enrichments-breach-add-processing-step",
        "Type": "Task",
        "Resource": module.lambda_enrichments.breach_processing_input_prep_func_arn
      },
      "cyberscan-enrichments-breach-add-processing-step": {
        "Next": "cyberscan-enrichments-breach-cluster-termination",
        "Type": "Task",
        "ResultPath": null,
        "Resource": "arn:aws:states:::elasticmapreduce:addStep.sync",
        "Parameters": {
          "ClusterId.$": "$.detail.emr.ClusterId",
          "Step": {
            "Name": "cyberscan-enrichments-breach-processing-step",
            "ActionOnFailure": "TERMINATE_CLUSTER",
            "HadoopJarStep": {
              "Jar": "command-runner.jar",
              "Args.$": "$.detail.sparkargs"
            }
          }
        }
      },
      "cyberscan-enrichments-breach-cluster-termination": {
        "End": true,
        "Type": "Task",
        "ResultPath": null,
        "Resource": "arn:aws:states:::elasticmapreduce:terminateCluster.sync",
        "Parameters": {
          "ClusterId.$": "$.detail.emr.ClusterId"
        }
      }
    }
  }


  )
}
