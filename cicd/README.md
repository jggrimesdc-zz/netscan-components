# Locally running the build container

You might want to test the docker container without having to run through the Gitlab CI pipeline.

## Pre-reqs

* Docker daemon

## Create the build image

The build image is created and deployed via gitlab ci's pipeline. To update the build image, create a branch
called `build-image`. Make any changes and push the branch to remote. Go to the pipeline page and manually run the
queued job for creating the build image.

*WARNING:*  Building a new build image will cause all future jobs to use the new image. Do this deliberately and with
caution.

## Compile documentation (locally)

```sh
node ./cicd/docgen.js
```

This will compile the documentation for sandbox by retrieving the base documentation from API Gateway and merging the
JSON documents within `src/scan/lambdas`.

The pipeline provides this script with arguments to change environments:

```
--aws_region 
--rest_api_id  
--api_deploy_stage_name
--s3_documentation_path
```

Note: these are retrieved from the terraform output. if the variable names change in terraform then they need to be
updated here as well.
