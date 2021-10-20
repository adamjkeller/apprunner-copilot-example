# Deploying a web service to AWS App Runner using the AWS Copilot CLI

## Create our application

```bash
copilot app init apprunner-demo
```

> **NOTE:** If you have a domain to have a vanity url for this demo, run the following:

```bash
copilot app init --domain domainname.com
```

## Create our environment

```bash
copilot env init --name test --profile default --default-config
```

## Create our service

```bash
copilot svc init --name user-api --svc-type "Request-Driven Web Service" --dockerfile ./Dockerfile
```

## Create our NoSQL Database table

```bash
copilot storage init -n users -t DynamoDB -w user-api --partition-key first_name:S --sort-key last_name:S --no-lsi
```

## Deploy our environment

```bash
copilot svc deploy
```

## Testing the application

#### Load the database

First, grab the url for your service.

```bash
lb_url=$(copilot svc show --name user-api --json | jq -r '.routes[0].url')
```

Run the following command to load the database:

```bash
curl -XPOST -s $lb_url/load_db
```

Now you can query the application by running the following commands:

#### Query specific user

```bash
curl -s "$lb_url/user/?first=Sheldon&last=Cooper"
```

#### Query all users

```bash
curl -s $lb_url/all_users
```

#### Load test the application and watch it scale

First, you will need a tool to load test the application.
For simplicity, I use [hey](https://github.com/rakyll/hey).

Run the following command to trigger 500 concurrent workers and 200k requests:

```bash
hey -n 200000 -c 500 https://dev.demo.adamjkeller.com/health
```

Head to the App Runner console and check out the metrics.
Watch the request count and Active instances metrics.
As the request count grows, active instances will begin to scale up to meet the demand.

## Deploy a CI/CD Pipeline

#### Create a fork of this repo

```bash
git remote add upstream <your-github-fork>
git push upstream HEAD
```

#### OPTIONAL: Create a production environment to demonstrate multi-environment deployments

```bash
copilot env init --name prod --profile default --prod
```

#### Initialize the pipeline, push the manifest to your fork, and build the pipeline

```bash
copilot pipeline init --app apprunner-demo --environments "test,prod" --git-branch main --url <git-remote-url-here>
```

#### Commit the pipeline configuration, and push to your repository

```bash
git add copilot
git commit -m "Adding copilot pipeline configuration"
git push
```

#### Deploy the pipeline!

```bash
copilot pipeline update --yes
```

#### Check status of pipeline

```bash
copilot pipeline status
```

## Cleanup

Run the following command to clean up the resources in the environment:

```bash
copilot app delete --name apprunner-demo --yes
```
