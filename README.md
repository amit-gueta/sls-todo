# sls-todo


Serverless TODO app, deploy by [serverless](https://www.serverless.com/)  
In order to run it, just run `serverless deploy`




How to use?


| Name | Path | HTTP Verb | Purpose |
| --- | --- | --- | --- |
| Registration | /signup | POST | User created |
| Confirmation | /confirm_signup | POST | User confirmation |
| Authentication | /auth | POST | User authentication |
| listAll | /todos | GET | List all TODO per user |
| Create | /create | POST | Create a TODO  |
| Get | /todos/:todoId | GET | Get specific TODO |
| Update | /todos/:todoId | PUT | Update specific  |
| Delete | /todos/:todoId | DELETE | Delete a TODO |

## Cognito Client Registration

- Cognito → Manage user pool → User pool → Client → Add app client

  - Please set "App client name" appropriately.
  - Do not check "Generate client secret".
  - Check all "Authentication flow settings".
  - "Prevent user presence error" is still enabled and there is no problem.
  - Register the client ID in the environment variable.


```shell
export CLIENT_ID=5ma31tppl2v2641mlp9q2jsa6q
```

## Registration

```shell
curl -H "Client-ID: ${CLIENT_ID}" \
-d '{"email":"your@email.com","password":"Passw0rd!@#"}' \
-X POST https://xxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/signup
```

- Response
  - Code: 200

## Confirmation

- code Will be sent to the email provided.
    - The email name is Verify your new account.

```shell
curl -H "Client-ID: ${CLIENT_ID}" \
-d '{"email":"your@email","code":"000000"}' \
-X POST https://xxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/confirm
```

- Response
  - Code: 200

## Authentication

```shell
curl -H "Client-ID: ${CLIENT_ID}" \
-d '{"email":"your@email.com","password":"Passw0rd!@#"}' \
-X POST https://xxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/auth
```

- Response

```json
{
  "idToken": "yyyyyyyyyy"
}
```

- For convenience, let's export the authentication token 

```shell
export ID_TOKEN=yyyyyyyyyy
```

## Create

- Request

```shell
curl -H "Authorization: ${ID_TOKEN}" \
-d '{"title":"fitness", "content":"back/leg"}' \
-X POST https://xxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/prod/todolists
```

- Response
  - Code: 201

## Index

- Request

```shell
curl -H "Authorization: ${ID_TOKEN}" \
-X GET 'https://xxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/prod/todolists'
```

- Response
  - Code: 200

```json
[
  {
    "content": "back/leg",
    "createdAt": 1587397379313,
    "todoId": "19858032-a05a-4951-aea4-f38d5d752997",
    "userId": "6dd25aab-62da-4e8a-a617-a393358a6a9d",
    "updatedAt": 1587397379313,
    "title": "fitness"
  }
]
```

## Show

- Request

```shell
curl -H "Authorization: ${ID_TOKEN}" \
-X GET 'https://xxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/prod/todolists/19858032-a05a-4951-aea4-f38d5d752997'
```

- Response
  - Code: 200

```json
{
  "content": "back/leg",
  "createdAt": 1587397379313,
  "todoId": "19858032-a05a-4951-aea4-f38d5d752997",
  "userId": "6dd25aab-62da-4e8a-a617-a393358a6a9d",
  "updatedAt": 1587397379313,
  "title": "fitness"
}
```

## Update

- Request

```shell
curl -H "Authorization: ${ID_TOKEN}" \
-d '{"content":"chest/shoulder"}' \
-X PATCH 'https://xxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/prod/todolists/19858032-a05a-4951-aea4-f38d5d752997'
```

- Response
  - Code: 204

## Destroy

- Request

```shell
curl -H "Authorization: ${ID_TOKEN}" \
-X DELETE 'https://xxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/prod/todolists/19858032-a05a-4951-aea4-f38d5d752997'
```

- Response
  - Code: 200
