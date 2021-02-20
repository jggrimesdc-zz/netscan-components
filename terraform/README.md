# Locally pushing infrastructure changes

## Pre-reqs

* AWS API Access to Sandbox
* Terraform CLI
* Python

## Setup

Initialize terraform to the `sandbox` environment by running:

```sh
./cicd/bootstrap.py sandbox
```

### Run a plan

Check if terraform is working by running a plan.

```sh
cd ./terraform
terraform plan
```

## Force unlocking the state

If you terminate a terraform process before it is complete then you may get a locking error on the next time you run
another terraform command.

If you get a locking state error, such as:

```ssh
Error: Error locking state: Error acquiring the state lock: ConditionalCheckFailedException: The conditional request failed
        status code: 400, request id: TR70QO6CM7Q6JMG31A3EO1QJGVVV4KQNSO5AEMVJF66Q9ASUAAJG
Lock Info:
  ID:        a309dc30-74a6-97b6-126f-d9a8aeee0c6c
  Path:      netscan-bucket/terraform/terraform.tfstate
  Operation: OperationTypePlan
  Version:   0.12.21
  Created:   2020-04-27 14:56:38.517321 +0000 UTC
  Info:      
```

Then you'll need to manually unlock the state using:

```ssh
terraform force-unlock <<lock-id>>
```

Where `lock-id` is the ID from the above error message. So the full command would look like:

```ssh
terraform force-unlock a309dc30-74a6-97b6-126f-d9a8aeee0c6c
```
