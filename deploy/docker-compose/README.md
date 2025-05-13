# docker-compose environment

The docker compose make easiser to develop the frontend and the backend using the following required compoments:

- keycloak
- opensearch and opensearch-dashboards
- minio

## Requirements before deploying

On your development workstation, we will need:

- [docker](https://docs.docker.com/engine/install/)
- [docker-compose](https://docs.docker.com/compose/install/)

## Steps to deploy

Increase the vm.max_map_count - this is a requirement for opensearch
```sh
sudo sysctl -w vm.max_map_count=262144
```

Add the entry 127.0.0.1 bidgpt-keycloak into /etc/hosts 
```sh
grep -q '127.0.0.1.*bidgpt-keycloak' /etc/hosts || echo "127.0.0.1 bidgpt-keycloak" | sudo tee -a /etc/hosts
```

Launch all containers
```sh
docker-compose up -d
```
## Access to the app

Some default users are already available and they can connect to bidgpt, opensearch-dashboards and minio:

- Administrator user : `alice`
- Editor user : `bob`
- Viewer user : `phil`

Hereunder the configuration of the following components required by bidgpt:

- Keycloak:
    - URL: http://localhost:8080
    - Admin service account: `admin`

- Opensearch:
    - URL: http://localhost:5601
    - Indice: `bidgpt-dev-metadata`
    - Admin service account: `admin`
    - Read only service account: `bidgpt_ro`
    - Read write service account: `bidgpt_rw`

- MinIO:
    - API URL: http://localhost:9000
    - WebUI URL: http://localhost:9001
    - Bucket: `bidgpt-dev-content`
    - Admin service account: `admin`
    - Read only service account: `bidgpt_ro`
    - Read write service account: `bidgpt_rw`

All passwords are `Azerty123_` for this ephemeral and local development stack.

## Setup you Visual Studio Code to use Dev Container

Simply install the dev container extension, check the docker container to attach the one you need, 
and to access to the react code, look in the '/src' for the react code or '/app' folder for the python code.
These are in the image. 

That should open your code editor as usual to the code. Any update on the code will be apllied to yoru local 
host git repository. 
