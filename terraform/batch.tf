locals {
  ecr_repo_image_name = "${var.aws_account}.dkr.ecr.${var.aws_region}.amazonaws.com/ingest_conform_repo:latest"
}

# setting up the iam role for ecs/batch communication
resource "aws_iam_role" "ecs_instance_role" {
    name               = "ecs_instance_role"
    description        = "Allows EC2 instances to call AWS services on your behalf."
    assume_role_policy = <<EOF
{
        "Version": "2012-10-17",
        "Statement": [
            {
            "Effect": "Allow",
            "Principal": {
                "Service": [
                "ecs-tasks.amazonaws.com",
                "ec2.amazonaws.com"
                ]
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
EOF
}

# taken from "s3purt" in Dev (for access to raw breach s3 bucket )
resource "aws_iam_policy" "breach_batch_bucket_policy" {
    name = "s3purt"
    description = "Policy to allow access for s3 bucket with raw breach files"

    policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:ListBucketVersions",
                "s3:ListBucket",
                "s3:GetBucketPolicy"
            ],
            "Resource": [
                "arn:aws:s3:::cyber-breach-data-set/*",
                "arn:aws:s3:::cyber-breach-data-set",
                "arn:aws:s3:us-east-2:694154633346:accesspoint/cyber-breach-data-set"
            ]
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "s3:ListAllMyBuckets",
            "Resource": "*"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "ecs_breach_s3_policy_attach" {
    role = aws_iam_role.ecs_instance_role.name
    policy_arn = aws_iam_policy.breach_batch_bucket_policy.arn
}

# assigning policies to the role
resource "aws_iam_role_policy_attachment" "ecs_instance_role_AmazonS3FullAccess" {
    role       = aws_iam_role.ecs_instance_role.name
    policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "ecs_instance_role_AWSBatchServiceRole" {
    role       = aws_iam_role.ecs_instance_role.name
    policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBatchServiceRole"
}

resource "aws_iam_role_policy_attachment" "ecs_instance_role_EC2ContainerServiceforEC2Role" {
    role       = aws_iam_role.ecs_instance_role.name
    policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

# setting up the AWS Batch Instance Role (correlates to ScanBatchServiceRole in Dev)
resource "aws_iam_instance_profile" "ecs_instance_role" {
    name = "ecs_instance_role"
    role = aws_iam_role.ecs_instance_role.name
}

# setting up the AWS Batch Service Role (correlates to AWSBatchServiceRole in Dev)
resource "aws_iam_role" "aws_batch_service_role" {
    name               = "aws_batch_service_role"
    assume_role_policy = <<EOF
{
        "Version": "2012-10-17",
        "Statement": [
            {
            "Effect": "Allow",
            "Principal": {
                "Service": "batch.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
            }
        ]
    }
EOF
}

# assigning policies to aws_batch_service_role
resource "aws_iam_role_policy_attachment" "aws_batch_service_role" {
    role       = aws_iam_role.aws_batch_service_role.name
    policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBatchServiceRole"
}

data "aws_security_group" "default" {
  # use below for vpc set up via terraform
  vpc_id = data.aws_vpc.selected_vpc.id

  filter {
    name   = "group-name"
    values = ["default"]
  }
}

# setting up the batch compute environment
resource "aws_batch_compute_environment" "ingest_compute_env" {

    # compute_environment_name = "ingest_compute_env_spot"
    compute_environment_name = "ingest_compute_env_ec2"

    compute_resources {
        instance_role = aws_iam_instance_profile.ecs_instance_role.arn

        instance_type = [
            "optimal"
        ]

        max_vcpus = 500
        min_vcpus = 0

        security_group_ids = [
            data.aws_security_group.default.id
            # aws_security_group.batch_security_group.id

        ]

        # use with all subnets
        subnets = [data.aws_subnet.selected_subnet.id]

        #code for ec2
        type                = "EC2"
        allocation_strategy = "BEST_FIT"
    }

    service_role = aws_iam_role.aws_batch_service_role.arn
    type         = "MANAGED"
    depends_on   = [aws_iam_role_policy_attachment.aws_batch_service_role]
}

# setting up the batch job queue
resource "aws_batch_job_queue" "ingest_conform_job_queue" {
    name                 = "ingest_conform_job_queue"
    state                = "ENABLED"
    priority             = 1
    compute_environments = [
        aws_batch_compute_environment.ingest_compute_env.arn
    ]
}

# set up the job definition - feodotracker
resource "aws_batch_job_definition" "feodotracker" {
    name = "reputation_feodotracker_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "feodotracker"
    })
}

# set up the job definition - urlhaus
resource "aws_batch_job_definition" "urlhaus" {
    name = "reputation_urlhaus_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
      image = local.ecr_repo_image_name
      job_role_arn = aws_iam_role.ecs_instance_role.arn,
      bucket = var.enrichment_bucket_name,
      label = "urlhaus"
    })
}

# set up the job definition - sslblacklist
resource "aws_batch_job_definition" "sslblacklist" {
    name = "reputation_sslblacklist_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "sslblacklist"
    })
}

# set up the job definition - sslipblacklist
resource "aws_batch_job_definition" "sslipblacklist" {
    name = "reputation_sslipblacklist_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "sslipblacklist"
    })
}

# set up the job definition - phishtank
resource "aws_batch_job_definition" "phishtank" {
    name = "reputation_phishtank_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "phishtank"
    })
}

# set up the job definition - cisco_ip
resource "aws_batch_job_definition" "cisco_ip" {
    name = "reputation_cisco_ip_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "cisco_ip"
    })
}

# set up the job definition - openphish
resource "aws_batch_job_definition" "openphish" {
    name = "reputation_openphish_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "openphish"
    })
}

# set up the job definition - alienvault
resource "aws_batch_job_definition" "alienvault" {
    name = "reputation_alienvault_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "alienvault"
    })
}

# set up the job definition - CVE-Modified
resource "aws_batch_job_definition" "CVE-Modified" {
    name = "vulnerability_CVE-Modified_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "CVE-Modified"
    })
}

# set up the job definition - CVE-Recent
resource "aws_batch_job_definition" "CVE-Recent" {
    name = "vulnerability_CVE-Recent_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "CVE-Recent"
    })
}

# set up the job definition - CVE-2020
resource "aws_batch_job_definition" "CVE-2020" {
    name = "vulnerability_CVE-2020_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "CVE-2020"
    })
}

# set up the job definition - CVE-2019
resource "aws_batch_job_definition" "CVE-2019" {
    name = "vulnerability_CVE-2019_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "CVE-2019"
    })
}

# set up the job definition - CVE-2018
resource "aws_batch_job_definition" "CVE-2018" {
    name = "vulnerability_CVE-2018_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "CVE-2018"
    })
}

# set up the job definition - CVE-2017
resource "aws_batch_job_definition" "CVE-2017" {
    name = "vulnerability_CVE-2017_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "CVE-2017"
    })
}

# set up the job definition - CVE-2016
resource "aws_batch_job_definition" "CVE-2016" {
    name = "vulnerability_CVE-2016_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "CVE-2016"
    })
}

# set up the job definition - CVE-2015
resource "aws_batch_job_definition" "CVE-2015" {
    name = "vulnerability_CVE-2015_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "CVE-2015"
    })
}

# set up the job definition - CVE-2014
resource "aws_batch_job_definition" "CVE-2014" {
    name = "vulnerability_CVE-2014_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "CVE-2014"
    })
}

# set up the job definition - CVE-2013
resource "aws_batch_job_definition" "CVE-2013" {
    name = "vulnerability_CVE-2013_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "CVE-2013"
    })
}

# set up the job definition - CVE-2012
resource "aws_batch_job_definition" "CVE-2012" {
    name = "vulnerability_CVE-2012_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "CVE-2012"
    })
}

# set up the job definition - CVE-2011
resource "aws_batch_job_definition" "CVE-2011" {
    name = "vulnerability_CVE-2011_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "CVE-2011"
    })
}

# set up the job definition - CVE-2010
resource "aws_batch_job_definition" "CVE-2010" {
    name = "vulnerability_CVE-2010_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "CVE-2010"
    })
}

# set up the job definition - CVE-2009
resource "aws_batch_job_definition" "CVE-2009" {
    name = "vulnerability_CVE-2009_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "CVE-2009"
    })
}

# set up the job definition - CVE-2008
resource "aws_batch_job_definition" "CVE-2008" {
    name = "vulnerability_CVE-2008_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "CVE-2008"
    })
}

# set up the job definition - CVE-2007
resource "aws_batch_job_definition" "CVE-2007" {
    name = "vulnerability_CVE-2007_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "CVE-2007"
    })
}

# set up the job definition - CVE-2006
resource "aws_batch_job_definition" "CVE-2006" {
    name = "vulnerability_CVE-2006_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "CVE-2006"
    })
}

# set up the job definition - CVE-2005
resource "aws_batch_job_definition" "CVE-2005" {
    name = "vulnerability_CVE-2005_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "CVE-2005"
    })
}

# set up the job definition - CVE-2004
resource "aws_batch_job_definition" "CVE-2004" {
    name = "vulnerability_CVE-2004_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "CVE-2004"
    })
}

# set up the job definition - CVE-2003
resource "aws_batch_job_definition" "CVE-2003" {
    name = "vulnerability_CVE-2003_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "CVE-2003"
    })
}

# set up the job definition - CVE-2002
resource "aws_batch_job_definition" "CVE-2002" {
    name = "vulnerability_CVE-2002_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "CVE-2002"
    })
}

# set up the job definition - blackarch
resource "aws_batch_job_definition" "blackarch" {
    name = "tool_blackarch_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "blackarch"
    })
}

# set up the job definition - kali
resource "aws_batch_job_definition" "kali" {
    name = "tool_kali_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "kali"
    })
}

# set up the job definition - cybergreen_daily
resource "aws_batch_job_definition" "cybergreen_daily" {
    name = "iihd_cybergreen_daily_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "cybergreen_daily"
    })
}

# set up the job definition - cybergreen_risk
resource "aws_batch_job_definition" "cybergreen_risk" {
    name = "iihd_cybergreen_risk_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "cybergreen_risk"
    })
}

# set up the job definition - cybergreen_asn
resource "aws_batch_job_definition" "cybergreen_asn" {
    name = "iihd_cybergreen_asn_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "cybergreen_asn"
    })
}

# set up the job definition - cybergreen historic
resource "aws_batch_job_definition" "cybergreen" {
    name = "iihd_cybergreen_job_definition"
    type = "container"

    container_properties = templatefile("templates/batch-container-definition-10000mib.tmpl", {
        image = local.ecr_repo_image_name
        job_role_arn = aws_iam_role.ecs_instance_role.arn,
        bucket = var.enrichment_bucket_name,
        label = "cybergreen"
    })
}
