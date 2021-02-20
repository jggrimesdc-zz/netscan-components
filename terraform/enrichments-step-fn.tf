resource "aws_s3_bucket_object" "cluster_bootstrap" {
  bucket       = var.enrichment_bucket_name
  key          = "scripts/cluster_bootstrap.sh"
  source       = "../src/scan/emr/cluster_bootstrap.sh"
  content_type = "text/x-shellscript"
  etag         = filemd5("../src/scan/emr/cluster_bootstrap.sh")
}

resource "aws_s3_bucket_object" "vuln_bootstrap" {
  bucket       = var.enrichment_bucket_name
  key          = "scripts/vuln_bootstrap.sh"
  source       = "../src/scan/emr/vuln_bootstrap.sh"
  content_type = "text/x-shellscript"
  etag         = filemd5("../src/scan/emr/vuln_bootstrap.sh")
}

resource "aws_s3_bucket_object" "postgresql_bootstrap" {
  bucket       = var.enrichment_bucket_name
  key          = "scripts/emr_postgresql_bootstrap.sh"
  source       = "../src/scan/emr/emr_postgresql_bootstrap.sh"
  content_type = "text/x-shellscript"
  etag         = filemd5("../src/scan/emr/emr_postgresql_bootstrap.sh")
}

resource "aws_sfn_state_machine" "cyberscan_enrichments" {
  name       = "cyberscan-enrichments-state-machine"
  role_arn   = aws_iam_role.cyberscan_enrichments_execution.arn
  definition = jsonencode(
  {
    "StartAt": "cyberscan-enrichments-which-document-type",
    "States": {
      "cyberscan-enrichments-which-document-type": {
        "Type": "Choice",
        "Choices": [
          {
            Variable: "$.detail.enrichment_type",
            StringEquals: "reputation",
            Next: "cyberscan-enrichments-reputation-cluster-creation"
          },
          {
            Variable: "$.detail.enrichment_type",
            StringEquals: "vulnerability",
            Next: "cyberscan-enrichments-vulnerability-cluster-creation"
          },
          {
            "Next": "cyberscan-enrichments-tool-cluster-creation",
            "StringEquals": "tools",
            "Variable": "$.detail.enrichment_type"
          },
          {
            "Next": "cyberscan-enrichments-threat-actor-cluster-creation",
            "StringEquals": "threat_actor",
            "Variable": "$.detail.enrichment_type"
          },
          {
            Variable: "$.detail.enrichment_type",
            StringEquals: "iihd",
            Next: "cyberscan-enrichments-iihd-cluster-creation"
          }
        ]
      },
      "cyberscan-enrichments-tool-cluster-creation": {
        "Next": "cyberscan-enrichments-tool-processing-input-prep",
        "Parameters": {
          "Applications": [
            {
              "Name": "spark"
            }
          ],
          "AutoScalingRole": aws_iam_role.cyberscan_enrichments_emr_role.name,
          "BootstrapActions": [
            {
              Name: "Custom Action",
              ScriptBootstrapAction: {
                "Path": "s3://${aws_s3_bucket_object.postgresql_bootstrap.bucket}/${aws_s3_bucket_object.postgresql_bootstrap.key}"
              }
            }
          ],
          "Instances": {
            "Ec2SubnetIds": [
              var.subnet_id
            ],
            "InstanceCount": 2,
            "KeepJobFlowAliveWhenNoSteps": true,
            "MasterInstanceType": "m5.xlarge",
            "SlaveInstanceType": "m5.xlarge"
          },
          "JobFlowRole": "EMR_EC2_DefaultRole",
          "Name": "cyberscan-enrichments-tool-cluster",
          "ReleaseLabel": "emr-5.30.1",
          "ServiceRole": aws_iam_role.cyberscan_enrichments_emr_role.name,
          "VisibleToAllUsers": true
        },
        "Resource": "arn:aws:states:::elasticmapreduce:createCluster.sync",
        "ResultPath": "$.detail.emr",
        "Type": "Task"
      },
      "cyberscan-enrichments-tool-processing-input-prep": {
        "Next":"cyberscan-enrichments-tool-add-processing-step",
        "Resource": module.lambda_enrichments.tool_processing_input_prep_func_arn,
        "Type": "Task",
        // if an error occurs at this step, the cluster shuts down 
        "Catch": [
          {
            "ErrorEquals": [
              "States.ALL"
            ],
            "Next": "cyberscan-enrichments-tool-cluster-termination"
          }
        ]
      },
      "cyberscan-enrichments-tool-add-processing-step": {
        "Next": "cyberscan-enrichments-tool-cluster-termination",
        "Parameters": {
          "ClusterId.$": "$.detail.emr.ClusterId",
          "Step": {
            "ActionOnFailure": "TERMINATE_CLUSTER",
            "HadoopJarStep": {
              "Args.$": "$.detail.sparkargs",
              "Jar": "command-runner.jar"
            },
            "Name": "cyberscan-enrichments-tool-processing-step"
          }
        },
        "Resource": "arn:aws:states:::elasticmapreduce:addStep.sync",
        "ResultPath": null,
        "Type": "Task"
      },
      "cyberscan-enrichments-tool-cluster-termination": {
        "End": true,
        "Parameters": {
          "ClusterId.$": "$.detail.emr.ClusterId"
        },
        "Resource": "arn:aws:states:::elasticmapreduce:terminateCluster.sync",
        "ResultPath": null,
        "Type": "Task"
      },
      "cyberscan-enrichments-reputation-cluster-creation": {
        "Next": "cyberscan-enrichments-reputation-processing-input-prep",
        "Type": "Task",
        "ResultPath": "$.detail.emr",
        "Resource": "arn:aws:states:::elasticmapreduce:createCluster.sync",
        "Parameters": {
          "Instances": {
            "Ec2SubnetIds": [
              var.subnet_id
            ],
            "InstanceCount": 2,
            "KeepJobFlowAliveWhenNoSteps": true,
            "MasterInstanceType": "m5.xlarge",
            "SlaveInstanceType": "m5.xlarge"
          },
          "JobFlowRole": "EMR_EC2_DefaultRole",
          "Name": "cyberscan-enrichments-reputation-cluster",
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
      "cyberscan-enrichments-reputation-processing-input-prep": {
        "Next": "cyberscan-enrichments-reputation-add-processing-step",
        "Type": "Task",
        "Resource":  module.lambda_enrichments.reputation_processing_input_prep_func_arn,
        // if an error occurs at this step, the cluster shuts down
        "Catch": [
          {
            "ErrorEquals": [
              "States.ALL"
            ],
            "Next": "cyberscan-enrichments-reputation-cluster-termination"
          }
        ]
      },
      "cyberscan-enrichments-reputation-add-processing-step": {
        "Next": "cyberscan-enrichments-reputation-cluster-termination",
        "Type": "Task",
        "ResultPath": null,
        "Resource": "arn:aws:states:::elasticmapreduce:addStep.sync",
        "Parameters": {
          "ClusterId.$": "$.detail.emr.ClusterId",
          "Step": {
            "Name": "cyberscan-enrichments-reputation-processing-step",
            "ActionOnFailure": "TERMINATE_CLUSTER",
            "HadoopJarStep": {
              "Jar": "command-runner.jar",
              "Args.$": "$.detail.sparkargs"
            }
          }
        }
      },
      "cyberscan-enrichments-reputation-cluster-termination": {
        "End": true,
        "Type": "Task",
        "ResultPath": null,
        "Resource": "arn:aws:states:::elasticmapreduce:terminateCluster.sync",
        "Parameters": {
          "ClusterId.$": "$.detail.emr.ClusterId"
        }
      },
      "cyberscan-enrichments-iihd-cluster-creation": {
        "Next": "cyberscan-enrichments-iihd-processing-input-prep",
        "Type": "Task",
        "ResultPath": "$.detail.emr",
        "Resource": "arn:aws:states:::elasticmapreduce:createCluster.sync",
        "Parameters": {
          "Instances": {
            "Ec2SubnetIds": [
              var.subnet_id
            ],
            "InstanceCount": 2,
            "KeepJobFlowAliveWhenNoSteps": true,
            "MasterInstanceType": "m5.xlarge",
            "SlaveInstanceType": "m5.xlarge"
          },
          "JobFlowRole": "EMR_EC2_DefaultRole",
          "Name": "cyberscan-enrichments-iihd-cluster",
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
      "cyberscan-enrichments-iihd-processing-input-prep": {
        "Next": "cyberscan-enrichments-iihd-add-processing-step",
        "Type": "Task",
        "Resource":  module.lambda_enrichments.iihd_processing_input_prep_func_arn,
        // if an error occurs at this step, the cluster shuts down
        "Catch": [
          {
            "ErrorEquals": [
              "States.ALL"
            ],
            "Next": "cyberscan-enrichments-iihd-cluster-termination"
          }
        ]
      },
      "cyberscan-enrichments-iihd-add-processing-step": {
        "Next": "cyberscan-enrichments-iihd-cluster-termination",
        "Type": "Task",
        "ResultPath": null,
        "Resource": "arn:aws:states:::elasticmapreduce:addStep.sync",
        "Parameters": {
          "ClusterId.$": "$.detail.emr.ClusterId",
          "Step": {
            "Name": "cyberscan-enrichments-iihd-processing-step",
            "ActionOnFailure": "TERMINATE_CLUSTER",
            "HadoopJarStep": {
              "Jar": "command-runner.jar",
              "Args.$": "$.detail.sparkargs"
            }
          }
        }
      },
      "cyberscan-enrichments-iihd-cluster-termination": {
        "End": true,
        "Type": "Task",
        "ResultPath": null,
        "Resource": "arn:aws:states:::elasticmapreduce:terminateCluster.sync",
        "Parameters": {
          "ClusterId.$": "$.detail.emr.ClusterId"
        }
      },
      "cyberscan-enrichments-vulnerability-cluster-creation": {
        "Next": "cyberscan-enrichments-vulnerability-processing-input-prep",
        "Type": "Task",
        "ResultPath": "$.detail.emr",
        "Resource": "arn:aws:states:::elasticmapreduce:createCluster.sync",
        "Parameters": {
          "Instances": {
            "Ec2SubnetIds": [
              var.subnet_id
            ],
            "InstanceCount": 2,
            "KeepJobFlowAliveWhenNoSteps": true,
            "MasterInstanceType": "m5.xlarge",
            "SlaveInstanceType": "m5.xlarge"
          },
          "JobFlowRole": "EMR_EC2_DefaultRole",
          "Name": "cyberscan-enrichments-vulnerability-cluster",
          "ServiceRole": aws_iam_role.cyberscan_enrichments_emr_role.name,
          "Applications": [
            {
              Name: "spark"
            }
          ],
          "AutoScalingRole": "cyberscan-enrichments-emr-role",
          "BootstrapActions": [
            {
              Name: "Custom Action",
              ScriptBootstrapAction: {
                "Path": "s3://${aws_s3_bucket_object.vuln_bootstrap.bucket}/${aws_s3_bucket_object.vuln_bootstrap.key}"
              }
            }
          ],
          "ReleaseLabel": "emr-5.30.1",
          "VisibleToAllUsers": true
        }
      },
      "cyberscan-enrichments-vulnerability-processing-input-prep": {
        "Next": "cyberscan-enrichments-vulnerability-add-processing-step",
        "Type": "Task",
        "Resource": module.lambda_enrichments.vulnerability_processing_input_prep_func_arn,
        // if an error occurs at this step, the cluster shuts down 
        "Catch": [
          {
            "ErrorEquals": [
              "States.ALL"
            ],
            "Next": "cyberscan-enrichments-vulnerability-cluster-termination"
          }
        ]
      },
      "cyberscan-enrichments-vulnerability-add-processing-step": {
        "Next": "cyberscan-enrichments-vulnerability-cluster-termination",
        "Type": "Task",
        "ResultPath": null,
        "Resource": "arn:aws:states:::elasticmapreduce:addStep.sync",
        "Parameters": {
          "ClusterId.$": "$.detail.emr.ClusterId",
          "Step": {
            "Name": "cyberscan-enrichments-vulnerability-processing-step",
            "ActionOnFailure": "TERMINATE_CLUSTER",
            "HadoopJarStep": {
              "Jar": "command-runner.jar",
              "Args.$": "$.detail.sparkargs"
            }
          }
        }
      },
      "cyberscan-enrichments-vulnerability-cluster-termination": {
        "End": true,
        "Type": "Task",
        "ResultPath": null,
        "Resource": "arn:aws:states:::elasticmapreduce:terminateCluster.sync",
        "Parameters": {
          "ClusterId.$": "$.detail.emr.ClusterId"
        }
      },
      "cyberscan-enrichments-threat-actor-cluster-creation": {
        "Next": "cyberscan-enrichments-threat-actor-processing-input-prep",
        "Parameters": {
          "Applications": [
            {
              "Name": "spark"
            }
          ],
          "AutoScalingRole": aws_iam_role.cyberscan_enrichments_emr_role.name,
          "BootstrapActions": [
            {
              Name: "Custom Action",
              ScriptBootstrapAction: {
                "Path": "s3://${aws_s3_bucket_object.postgresql_bootstrap.bucket}/${aws_s3_bucket_object.postgresql_bootstrap.key}"
              }
            }
          ],
          "Instances": {
            "Ec2SubnetIds": [
              var.subnet_id
            ],
            "InstanceCount": 2,
            "KeepJobFlowAliveWhenNoSteps": true,
            "MasterInstanceType": "m5.xlarge",
            "SlaveInstanceType": "m5.xlarge"
          },
          "JobFlowRole": "EMR_EC2_DefaultRole",
          "Name": "cyberscan-enrichments-threat-actor-cluster",
          "ReleaseLabel": "emr-5.30.1",
          "ServiceRole": aws_iam_role.cyberscan_enrichments_emr_role.name,
          "VisibleToAllUsers": true
        },
        "Resource": "arn:aws:states:::elasticmapreduce:createCluster.sync",
        "ResultPath": "$.detail.emr",
        "Type": "Task"
      },
      "cyberscan-enrichments-threat-actor-processing-input-prep": {
        "Next":"cyberscan-enrichments-threat-actor-add-processing-step",
        "Resource": module.lambda_enrichments.threat_actor_processing_input_prep_func_arn, 
        "Type": "Task",
        // if an error occurs at this step, the cluster shuts down 
        "Catch": [
          {
            "ErrorEquals": [
              "States.ALL"
            ],
            "Next": "cyberscan-enrichments-threat-actor-cluster-termination"
          }
        ]
      },
      "cyberscan-enrichments-threat-actor-add-processing-step": {
        "Next": "cyberscan-enrichments-threat-actor-cluster-termination",
        "Type": "Task",
        "ResultPath": null,
        "Resource": "arn:aws:states:::elasticmapreduce:addStep.sync",
        "Parameters": {
          "ClusterId.$": "$.detail.emr.ClusterId",
          "Step": {
            "ActionOnFailure": "TERMINATE_CLUSTER",
            "HadoopJarStep": {
              "Args.$": "$.detail.sparkargs",
              "Jar": "command-runner.jar"
            },
            "Name": "cyberscan-enrichments-threat-actor-processing-step"
          }
        }
      },
      "cyberscan-enrichments-threat-actor-cluster-termination": {
        "End": true,
        "Type": "Task",
        "ResultPath": null,
        "Resource": "arn:aws:states:::elasticmapreduce:terminateCluster.sync",
        "Parameters": {
          "ClusterId.$": "$.detail.emr.ClusterId"
        }
      }
    }
  })
}
