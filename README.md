# foodfight-serverless

This is a recreation of the classic BBS door game "Food Fight", using the serverless framework to deploy Lambda functions with a DynamoDB backend.

## Structure

This service has a separate directory for all the user operations. For each operation exactly one file exists e.g. `user/delete.py`. In each of these files there is exactly one function defined.

The idea behind the `user` directory is that in the future, there will be a separate directory with individual functions based on fights, upgrades, etc.


## Setup

Follow the official [Serverless installation instructions](https://serverless.com/framework/docs/providers/aws/guide/installation/) to ensure you have the Serverless NPM package installed, along with your AWS credentials set up on your local machine.

## Deploy

In order to deploy the endpoint, run

```bash
sls deploy
```

The expected result should be similar to:

```bash
Serverless: Packaging service…
Serverless: Uploading CloudFormation file to S3…
Serverless: Uploading service .zip file to S3…
Serverless: Updating Stack…
Serverless: Checking Stack update progress…
Serverless: Stack update finished…

Service Information
service: foodfight-serverless
stage: dev
region: us-east-1
api keys:
  None
endpoints:
  POST - https://45wf34z5yf.execute-api.us-east-1.amazonaws.com/dev/user
  GET - https://45wf34z5yf.execute-api.us-east-1.amazonaws.com/dev/user
  GET - https://45wf34z5yf.execute-api.us-east-1.amazonaws.com/dev/user/{username}
  PUT - https://45wf34z5yf.execute-api.us-east-1.amazonaws.com/dev/user/{username}
  DELETE - https://45wf34z5yf.execute-api.us-east-1.amazonaws.com/dev/user/{username}
functions:
  user-create: foodfight-serverless-dev-user-create
  user-list: foodfight-serverless-dev-user-list
  user-get: foodfight-serverless-dev-user-get
  user-update: foodfight-serverless-dev-user-update
  user-delete: foodfight-serverless-dev-user-delete
```

## Usage

You can create, retrieve, update, or delete users with the following commands:

### Create a User

```bash
curl -X POST https://XXXXXXX.execute-api.us-east-1.amazonaws.com/dev/user --data '{ "username": "whatever" }'
```

No output

### List all Users

```bash
curl https://XXXXXXX.execute-api.us-east-1.amazonaws.com/dev/user
```

Example output:
```bash
[{"createdAt": 1560477784347, "username": "cparlette", "updatedAt": 1560480556172, "weapon": 2, "armor": 3}, {"createdAt": 1560541863727, "username": "obsidian", "weapon": 1, "updatedAt": 1560541863727, "armor": 1}]%
```

### Get one User

```bash
# Replace the <username> part with a real username from your user table
curl https://XXXXXXX.execute-api.us-east-1.amazonaws.com/dev/user/<username>
```

Example Result:
```bash
{"createdAt": 1560477784347, "username": "cparlette", "weapon": 1, "updatedAt": 1560477784347, "armor": 1}%
```

### Update a User

```bash
# Replace the <username> part with a real username from your user table
curl -X PUT https://XXXXXXX.execute-api.us-east-1.amazonaws.com/dev/user/<username> --data '{ "weapon": 2, "armor": 3 }'
```

Example Result:
```bash
{"createdAt": 1560477784347, "username": "cparlette", "updatedAt": 1560480556172, "weapon": 2, "armor": 3}%
```

### Delete a User

```bash
# Replace the <username> part with a real username from your user table
curl -X DELETE https://XXXXXXX.execute-api.us-east-1.amazonaws.com/dev/user/<username>
```

No output

## References used

Originally modified from [an official Serverless example](https://github.com/serverless/examples/tree/master/aws-python-rest-api-with-dynamodb)