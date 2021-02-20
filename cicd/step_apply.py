#!/usr/bin/python3

import re
import subprocess

import bootstrap


# Transform terraform output to command-line style arguments
# api_deploy_stage_name = sandbox
# aws_region = us-east-1
# rest_api_id = c1tydbup25
# s3_documentation_path = terraform-dev-qos/apigateway-docs
def build_args_from_terraform_output(stdout):
    raw = stdout.splitlines()
    raw = re.sub("b'|'|^\[|\]$", "", str(raw))
    raw = re.sub(' = ', '=', raw)
    return '--' + ' --'.join(raw.split(', '))


bootstrap.initialize()

# force redeployment of API
cmd = "terraform taint aws_api_gateway_deployment.cs_api_root_stage_qa"
subprocess.check_call(cmd.split())

cmd = "terraform apply -auto-approve"
subprocess.check_call(cmd.split())

cmd = "terraform output -no-color"
output = subprocess.check_output(cmd.split())

args = build_args_from_terraform_output(output)
cmd = "node ../cicd/docgen.js " + args
subprocess.check_call(cmd.split())
