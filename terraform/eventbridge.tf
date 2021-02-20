//////////////////////////
// EVENTBRIDGE CF STACK //
//////////////////////////

locals {
  ingest_conform_job_queue_arn = "arn:aws:batch:${local.aws_region}:${var.aws_account}:job-queue/ingest_conform_job_queue"
}

# setting up eventbridge - batch role
resource "aws_iam_role" "eventbridge_batch_role" {
  name = "Eventbridge_Invoke_Batch_Job_Role"

  assume_role_policy = <<EOF
{
        "Version": "2012-10-17",
        "Statement": [
        {
            "Action": "sts:AssumeRole",
            "Principal": {
                "Service": "events.amazonaws.com"
            },
            "Effect": "Allow",
            "Sid": ""

        }
    ]
}
EOF
}

resource "aws_iam_policy" "eventbridge_batch_policy" {
  name        = "Eventbridge_Invoke_Batch_Job_Policy"
  description = "Policy for Eventbridge to invoke Batch Jobs"

  policy = <<EOF
{
        "Version": "2012-10-17",
        "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "batch:SubmitJob"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "eventbridge_batch_policy_attach" {
  role       = aws_iam_role.eventbridge_batch_role.name
  policy_arn = aws_iam_policy.eventbridge_batch_policy.arn
}

resource "aws_cloudformation_stack" "event_bridge" {
  name          = "event-bridge-stack"
  template_body = jsonencode(
  {
    "Resources": {
      "cyberscanscorerule1C59F356": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "EventBusName": "cyberscan-event-bus"
          "EventPattern": {
            "detail-type": [
              "Trigger Downstream Analytics"
            ],
            "source": [
              "COLLECTOR_S3_WRITE_COMPLETE_RECEIVER"
            ]
          },
          "State": "ENABLED",
          "Targets": [
            {
              Id: "Target0",
              RoleArn: aws_sfn_state_machine.cs_scoring_pipeline.role_arn
              Arn: "arn:aws:states:${local.aws_region}:${var.aws_account}:stateMachine:${aws_sfn_state_machine.cs_scoring_pipeline.name}"
            }
          ]
        }
      },
      "scanscheduler": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "EventBusName": "default"
          "Description": "Periodically checks for scans to be submitted.",
          "ScheduleExpression": "rate(1 hour)",
          "State": "ENABLED",
          "Targets": [
            {
              Id: "Id98fc3cf5-f1d3-4a3c-b845-845f94378e4e",
              Arn: "arn:aws:lambda:${var.aws_region}:${var.aws_account}:function:meta_schedule_querier"
            }
          ]
        }
      },
      "cyberscanenrichmentsrule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "EventBusName": "cyberscan-event-bus"
          "EventPattern": {
            "detail-type": [
              "Enrichment S3 PutObject Notification"
            ],
            "source": [
              "cyberscan.sns"
            ]
          },
          "State": "DISABLED",
          "Targets": [
            {
              Id: "Target1"
              RoleArn: aws_sfn_state_machine.cs_scoring_pipeline.role_arn
              Arn: "arn:aws:states:${local.aws_region}:${var.aws_account}:stateMachine:${aws_sfn_state_machine.cyberscan_enrichments.name}"
            }
          ]
        }
      },
      "reputationfeodotrackerrule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 * * ? *)",
          "Description": "Runs the ingest and conform script daily at 1:00 am UTC for feodotracker from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "feodotracker_rule_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.feodotracker.arn,
                JobName: "reputation_feodotracker_job"
              }
            }
          ]
        }
      },
      "reputationurlhausrule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 * * ? *)",
          "Description": "Runs the ingest and conform script daily at 1:00 am UTC for urlhaus from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Id: "reputationurlhaus_rule_id",
              Arn: local.ingest_conform_job_queue_arn,
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.urlhaus.arn,
                JobName: "reputation_urlhaus_job"
              }
            }
          ]
        }
      },
      "reputationsslblacklistrule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 * * ? *)",
          "Description": "Runs the ingest and conform script daily at 1:00 am UTC for sslblacklist from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "sslblacklist_rule_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.sslblacklist.arn,
                JobName: "reputation_sslblacklist_job"
              }
            }
          ]
        }
      },
      "reputationsslipblacklistrule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 * * ? *)",
          "Description": "Runs the ingest and conform script daily at 1:00 am UTC for sslipblacklist from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "sslipblacklist_rule_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.sslipblacklist.arn,
                JobName: "reputation_sslipblacklist_job"
              }
            }
          ]
        }
      },
      "reputationphishtankrule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 * * ? *)",
          "Description": "Runs the ingest and conform script daily at 1:00 am UTC for phishtank from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "phishtank_rule_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.phishtank.arn,
                JobName: "reputation_phishtank_job"
              }
            }
          ]
        }
      },
      "reputationciscoiprule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 * * ? *)",
          "Description": "Runs the ingest and conform script daily at 1:00 am UTC for cisco_ip from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "cisco_ip_rule_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.cisco_ip.arn,
                JobName: "reputation_cisco_ip_job"
              }
            }
          ]
        }
      },
      "reputationopenphishrule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 * * ? *)",
          "Description": "Runs the ingest and conform script daily at 1:00 am UTC for openphish from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "openphish_ip_rule_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.openphish.arn,
                JobName: "reputation_openphish_job"
              }
            }
          ]
        }
      },
      "reputationalienvaultrule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 * * ? *)",
          "Description": "Runs the ingest and conform script daily at 1:00 am UTC for alienvault from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "alienvault_ip_rule_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.alienvault.arn,
                JobName: "reputation_alienvault_job"
              }
            }
          ]
        }
      },
      "vulnerabilityCVEModifiedrule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 * * ? *)",
          "Description": "Runs the ingest and conform script daily at 1:00 am UTC for CVE-Modified from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "CVE-Modified_ip_rule_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.CVE-Modified.arn,
                JobName: "reputation_CVE-Modified_job"
              }
            }
          ]
        }
      },
      "vulnerabilityCVERecentrule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 * * ? *)",
          "Description": "Runs the ingest and conform script daily at 1:00 am UTC for CVE-Recent from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "CVE-Recent_ip_rule_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.CVE-Recent.arn,
                JobName: "reputation_CVE-Recent_job"
              }
            }
          ]
        }
      },
      "vulnerabilityCVE2020rule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 1 1 ? *)",
          "Description": "Runs the ingest and conform script yearly at 1:00 am UTC Jan 1st for CVE-2020 from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "CVE-2020_ip_rule_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.CVE-2020.arn,
                JobName: "reputation_CVE-2020_job"
              }
            }
          ]
        }
      },
      "vulnerabilityCVE2019rule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 1 1 ? *)",
          "Description": "Runs the ingest and conform script yearly at 1:00 am UTC Jan 1st for CVE-2019 from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "CVE-2019_ip_rule_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.CVE-2019.arn,
                JobName: "reputation_CVE-2019_job"
              }
            }
          ]
        }
      },
      "vulnerabilityCVE2018rule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 1 1 ? *)",
          "Description": "Runs the ingest and conform script yearly at 1:00 am UTC Jan 1st for CVE-2018 from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "CVE-2018_ip_rule_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.CVE-2018.arn,
                JobName: "reputation_CVE-2018_job"
              }
            }
          ]
        }
      },
      "vulnerabilityCVE2017rule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 1 1 ? *)",
          "Description": "Runs the ingest and conform script yearly at 1:00 am UTC Jan 1st for CVE-2017 from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "CVE-2017_ip_rule_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.CVE-2017.arn,
                JobName: "reputation_CVE-2017_job"
              }
            }
          ]
        }
      },
      "vulnerabilityCVE2016rule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 1 1 ? *)",
          "Description": "Runs the ingest and conform script yearly at 1:00 am UTC Jan 1st for CVE-2016 from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "CVE-2016_ip_rule_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.CVE-2016.arn,
                JobName: "reputation_CVE-2016_job"
              }
            }
          ]
        }
      },
      "vulnerabilityCVE2015rule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 1 1 ? *)",
          "Description": "Runs the ingest and conform script yearly at 1:00 am UTC Jan 1st for CVE-2015 from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "CVE-2015_ip_rule_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.CVE-2015.arn,
                JobName: "reputation_CVE-2015_job"
              }
            }
          ]
        }
      },
      "vulnerabilityCVE2014rule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 1 1 ? *)",
          "Description": "Runs the ingest and conform script yearly at 1:00 am UTC Jan 1st for CVE-2014 from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "CVE-2014_ip_rule_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.CVE-2014.arn,
                JobName: "reputation_CVE-2014_job"
              }
            }
          ]
        }
      },
      "vulnerabilityCVE2013rule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 1 1 ? *)",
          "Description": "Runs the ingest and conform script yearly at 1:00 am UTC Jan 1st for CVE-2013 from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "CVE-2013_ip_rule_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.CVE-2013.arn,
                JobName: "reputation_CVE-2013_job"
              }
            }
          ]
        }
      },
      "vulnerabilityCVE2012rule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 1 1 ? *)",
          "Description": "Runs the ingest and conform script yearly at 1:00 am UTC Jan 1st for CVE-2012 from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "CVE-2012_ip_rule_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.CVE-2012.arn,
                JobName: "reputation_CVE-2012_job"
              }
            }
          ]
        }
      },
      "vulnerabilityCVE2011rule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 1 1 ? *)",
          "Description": "Runs the ingest and conform script yearly at 1:00 am UTC Jan 1st for CVE-2011 from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "CVE-2011_ip_rule_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.CVE-2011.arn,
                JobName: "reputation_CVE-2011_job"
              }
            }
          ]
        }
      },
      "vulnerabilityCVE2010rule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 1 1 ? *)",
          "Description": "Runs the ingest and conform script yearly at 1:00 am UTC Jan 1st for CVE-2010 from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "CVE-2010_ip_rule_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.CVE-2010.arn,
                JobName: "reputation_CVE-2010_job"
              }
            }
          ]
        }
      },
      "vulnerabilityCVE2009rule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 1 1 ? *)",
          "Description": "Runs the ingest and conform script yearly at 1:00 am UTC Jan 1st for CVE-2009 from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "CVE-2009_ip_rule_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.CVE-2009.arn,
                JobName: "reputation_CVE-2009_job"
              }
            }
          ]
        }
      },
      "vulnerabilityCVE2008rule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 1 1 ? *)",
          "Description": "Runs the ingest and conform script yearly at 1:00 am UTC Jan 1st for CVE-2008 from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "CVE-2008_ip_rule_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.CVE-2008.arn,
                JobName: "reputation_CVE-2008_job"
              }
            }
          ]
        }
      },
      "vulnerabilityCVE2007rule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 1 1 ? *)",
          "Description": "Runs the ingest and conform script yearly at 1:00 am UTC Jan 1st for CVE-2007 from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "CVE-2007_ip_rule_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.CVE-2007.arn,
                JobName: "reputation_CVE-2007_job"
              }
            }
          ]
        }
      },
      "vulnerabilityCVE2005rule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 1 1 ? *)",
          "Description": "Runs the ingest and conform script yearly at 1:00 am UTC Jan 1st for CVE-2005 from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "CVE-2005_ip_rule_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.CVE-2005.arn,
                JobName: "reputation_CVE-2005_job"
              }
            }
          ]
        }
      },
      "vulnerabilityCVE2004rule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 1 1 ? *)",
          "Description": "Runs the ingest and conform script yearly at 1:00 am UTC Jan 1st for CVE-2004 from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "CVE-2004_ip_rule_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.CVE-2004.arn,
                JobName: "reputation_CVE-2004_job"
              }
            }
          ]
        }
      },
      "vulnerabilityCVE2003rule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 1 1 ? *)",
          "Description": "Runs the ingest and conform script yearly at 1:00 am UTC Jan 1st for CVE-2003 from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "CVE-2003_ip_rule_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.CVE-2003.arn,
                JobName: "reputation_CVE-2003_job"
              }
            }
          ]
        }
      },
      "vulnerabilityCVE2002rule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 1 1 ? *)",
          "Description": "Runs the ingest and conform script yearly at 1:00 am UTC Jan 1st for CVE-2002 from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "CVE-2002_ip_rule_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.CVE-2002.arn,
                JobName: "reputation_CVE-2002_job"
              }
            }
          ]
        }
      },
      "toolblackarchrule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 0 1 * ? *)",
          "Description": "Runs the ingest and conform script monthly at 00:00 am UTC on the first for blackarch from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "blackarch_rule_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.blackarch.arn,
                JobName: "tool_blackarch_job"
              }
            }
          ]
        }
      },
      "toolkalirule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 1 * ? *)",
          "Description": "Runs the ingest and conform script monthly at 01:00 am UTC on the first for kali from tf",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "kali_rule_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.kali.arn,
                JobName: "tool_kali_job"
              }
            }
          ]
        }
      },
      "iihdcybergreenriskrule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "rate(365 days)",
          "Description": "Runs the ingest and conform script once a year for the cybergreen_risk data",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "iihd_cybergreen_risk_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.cybergreen_risk.arn,
                JobName: "iihd_cybergreen_risk_job"
              }
            }
          ]
        }
      },
      "iihdcybergreenasnrule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "rate(365 days)",
          "Description": "Runs the ingest and conform script once a year for the cybergreen asn data",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "iihd_cybergreen_asn_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.cybergreen_asn.arn,
                JobName: "iihd_cybergreen_asn_job"
              }
            }
          ]
        }
      },
      "iihdcybergreendailyrule": {
        "Type": "AWS::Events::Rule",
        "Properties": {
          "ScheduleExpression": "cron(0 1 * * ? *)",
          "Description": "Runs the ingest and conform script daily at 1:00 am UTC for cybergreen daily",
          "State": "ENABLED",
          "Targets": [
            {
              Arn: local.ingest_conform_job_queue_arn,
              Id: "iihd_cybergreen_daily_id",
              RoleArn: aws_iam_role.eventbridge_batch_role.arn,
              BatchParameters: {
                JobDefinition: aws_batch_job_definition.cybergreen_daily.arn,
                JobName: "iihd_cybergreen_daily_job"
              }
            }
          ]
        }
      }
    }
  }
  )
}
