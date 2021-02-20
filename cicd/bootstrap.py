#!/usr/bin/python3
#
# Bootstraps the Terraform environment:
# - Symlinks the correct environment variables to be automatically used by every terraform command
# - Runs a `terraform init` with the correct backend config for the given environment

import os
import subprocess
import sys


def check_arguments():
    environments = ['sandbox', 'dev', 'qa', 'mt-prod']
    errorMsg = 'Missing valid environment argument.  Valid environments are: ' + ', '.join(environments)

    if len(sys.argv) < 2 or sys.argv[1].lower() not in environments:
        raise ValueError(errorMsg)


def initialize():
    check_arguments()
    env = sys.argv[1].lower()

    # change to root directory of project
    filedir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(filedir + '/../terraform')

    # symlink environment variables to be used automatically by terraform
    cmd = "ln -sf ./config/" + env + ".terraform.tfvars.json ./terraform.auto.tfvars.json"
    subprocess.check_call(cmd.split())

    # initialize terraform
    cmd = "terraform init -backend-config=config/" + env + ".backend.config"
    process = subprocess.check_call(cmd.split())

    print("\nTerraform initialized to '" + env + "' environment.\n")


# ran as a script
if __name__ == '__main__':
    initialize()
