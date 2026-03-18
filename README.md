# DBOS

Test repo trailing DBOS workflows to replace Airflow for orchestrating an EMR-Serverless env

## Getting Started

```bash
docker-compose build
docker-compoe up -d
```

## Setting up your env files

Create the following files:

```
.envs/conductor.env
.envs/app.env
```

Go to `https://console.dbos.dev` and signup for an account, then head to `https://console.dbos.dev/settings/license-key` and generate a licence key. Add the licence key to `conductor.env` like so:

```
DBOS_CONDUCTOR_LICENSE_KEY=<LICENCE_KEY>
```

Now you need to start up the docker containers:

```bash
docker-compose build
docker-compoe up -d
```

and head to `http://localhost/settings/apikey` once the console container has started and generate an API key. This key should be added to `app.env` like so:

```
CONDUCTOR_KEY=<API_KEY>

```

Now run `docker-compose up -d` again and all the containers should be able to communicate.

Next you have to connect the application on the console by heading to `http://localhost/conductor/register` and entering `kdp-workflows` as the application name. This will then register the application to the console and allow monitoring of workflows
