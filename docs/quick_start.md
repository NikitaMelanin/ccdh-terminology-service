# Quick start

## System dependencies
- [Docker](https://www.docker.com/products/docker-desktop): Needs to be running in 
  the background on your machinewhen running `docker-compose`. We recommend 
  [Docker Desktop](https://www.docker.com/products/docker-desktop) for Windows and Mac.
- [Python 3.7+](https://www.python.org/downloads/)
- [Neo4J 4.0+](https://neo4j.com/download/)

## Cloning and setting up git submodules
Clone this repo, and pull the submodules. 

```shell
git clone https://github.com/cancerDHC/ccdh-terminology-service.git
cd ccdh-terminology-service 
git submodule update --init --recursive
```

Because the PDC json files are under Git LFS (Large File Storage), it must be
installed in the repository. Follow [these instructions](https://git-lfs.github.com/)
for installing Git LFS on your machine. Then, install it in the repo via 
`git lfs install`. Then, pull the content with git lfs.

```shell
cd crdc-nodes/PDC-Public/documentation/prod/json
git lfs pull --include ./*.json
cd -  # to return to root diriectory of repo
```

## Using Docker
### Seeding Neo4j vlumes 
This is the prefered approach to set up the service. You need to have
docker and docker-compose installed on your system before the set up. 

First copy the TCCM NCIT Turtle RDF to the docker import directory for neo4j. 

```shell
cp data/tccm/ncit-termci.ttl docker/volumes/prod/neo4j/import
cp data/tccm/ncit-termci.ttl docker/volumes/test/neo4j/import
```

## Environmental variables
In the root directory, Create a file called `.env.prod` file with required 
environment variables.

The `.env.prod` file should contain the following:

```shell
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=<password>
NEO4J_HOST=ccdh-neo4j
NEO4J_BOLT_PORT=7687
REDIS_URL=redis://ccdh-redis:6379
USER_ACCESS_TOKEN=<token>
```

Choose and `<password>`. As for the `<token>` to put under `USER_ACCESS_TOKEN`, 
this is used for [GitHub workflow integration](https://docs.github.com/en/actions/reference/authentication-in-a-workflow) 
with the [CCDH Model repository](https://github.com/cancerDHC/ccdhmodel). If you 
have access to that repository, you should use a 
[GitHub personal access token](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token) 
and set `USER_ACCESS_TOKEN` to that. The port, host, and 'bolt uri' have been 
auto-filled for you, but these are configurable if you want to change them.

By default, the importer will pull the CRDC-H YAML from the main branch of the 
ccdhmodel GitHub repo. 
If another branch is preferred, you can add this line in the .env file.

```shell
CCDHMODEL_BRANCH=ccdhmodel_branch_name_or_full_sha_commit_id
```

Finally, in addition to `.env.prod`, you'll also need a file called `.env`. This 
is due to some limitations in the docker setup. We want the docker-compose files
to point to distinctly different .env files, but it also requires a generic file
called `.env`, even if you tell it to look for another file. So you should run:

```sh
cp .env.prod .env
```

And finally, the current setup also expects an `.env.test`, even if you're just running
a single instance of the docker containers. This really shouldn't be needed if
runnin a single instance, but for now it is needed. So finally, run:

```shell
cdp .env.prod .env.test
```

## Running containers
Then run the docker-compose build to build the images

```shell
make deploy-local
```

After the docker containers are up, log onto the ccdh-api container and load data. 

```shell
docker exec -it ccdh-api /bin/bash
python -m ccdh.importers.importer
```

After data is loaded, the server will be running on a local port at 7070. You can visit
[http://localhost:7070](http://localhost:7070). 

## Useful tools
You may find it useful to also install the following:
- Docker desktop
- Neo4j desktop / Neo4j browser

## Debugging locally
If you want to debug locally, you should run the CCDH-API outside of docker. That 
way, if you set breakpoints in your IDE, it will stop at them.

**Step 1: `.env.dev`**
1.1. Create an `.env.dev` file. It can look like just like your `.env.prod` file, but
with the following change:

```sh
NEO4J_HOST=localhost
```

1.2. Then, do: `cp .env.dev .env`

**Step 2: Run**
From within your IDE's debugger, have it run the following command:
```sh
uvicorn ccdh.api.app:app $$ROOT_PATH --host 0.0.0.0 --port 8000
```
