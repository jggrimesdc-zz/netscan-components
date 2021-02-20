# Scan Components

## Updating the Docker build image

Make any changes you need to the `Dockerfile` at the project's root directory. Updating the build image is only
necessary when extra tooling is required by the build process.

First step is to login to Gitlab's registry. You'll be prompted for your username and password.

```shell script
docker login registry.gitlab.com
```

Then, locally build the docker image.

```shell script
docker build -t registry.gitlab.com/netscan/teams/wcaas/netscan-components .
```

And finally, push it to gitlab.

```shell script
docker push registry.gitlab.com/netscan/teams/wcaas/netscan-components
```

Make sure that `.gitlab-ci.yml` is either pointing to `latest` or your specific tag.

## ADR

To update the ADR index.md file, run `adr-log -d doc/adr -i` in the project root. This command will read all of the
markdown files in the `doc/adr` directory that begin with an integer. These files are considered to be ADR documents.

Build ADRs in accordance with `doc/adr/template.md` and run the `adr-log -d doc/adr -i` command to update the
documentation.
