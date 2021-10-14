# AWS App Runner using AWS Copilot CLI Demo

## Create our application

```bash
copilot app init --name apprunner-demo
```

> **NOTE:** If you have a domain to have a vanity url for this demo, run the following:

```bash
copilot app init --domain domainname.com
```

## Create our environment

```bash
copilot env init --name test
```

## Create our service

```bash
copilot svc init --name user-api --svc-type "Request-Driven Web Service" --dockerfile ./Dockerfile
```

## Create our NoSQL Database table

```bash
copilot storage init -n users -t DynamoDB -w users-api --partition-key first_name:S --sort-key last_name:S --no-lsi
```

## Deploy our environment

```bash
copilot svc deploy
```

## Testing the application

#### Load the database

First, grab the url for your service.
Run the following command to load the database:

```bash
curl -XPOST -s http://<url>/load_db
```

Now you can query the application by running the following commands:

#### Query specific user

curl -s 'http://<url>/user/?first=Sheldon&last=Cooper'

#### Query all users

curl -s http://<url>/all_users
