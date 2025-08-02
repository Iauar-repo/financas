# Endpoints
- Authentication
    - [POST - /auth/login](#post-authlogin)
    - [POST - /auth/refresh](#post-authrefresh)
    - [POST - /auth/logout](#post-authlogout)
    - [GET - /auth/me](#get-authme)
    - [GET - /auth/confirm/\<token\>](#get-authconfirmtoken)
    - [POST - /auth/resend](#post-authresend)
    - [POST - /auth/callback/google](#post-authcallbackgoogle)
- Users
    - [GET - /users/](#get-users)
    - [POST - /users/register](#post-usersregister)
    - [GET - /users/\<user_id\>](#get-usersid)
    - [PATCH - /users/<user_id>](#patch-usersid)
    - [DELETE - /users/<user_id>](#delete-usersid)

## Base API URL

Default port: `5000` \
Current version: `api/v1`

http://127.0.0.1:5000/api/v1

## Authentication

### POST `/auth/login`

Authenticate a user with `email` and `password`.

#### Request
```json
{
    "email": "email@email.com",
    "password": "123"
}
```

#### Response
```json
{
    "data": {
        "access_token": "xxx",
        "refresh_token": "yyy"
    },
    "message": "Operation successful."
}
```
---

### POST `/auth/refresh`

Generate new tokens for a `refresh_token`.

#### Headers
`Authorization: Bearer <refresh_token>`

#### Response
```json
{
    "data": {
        "access_token": "xxx",
        "refresh_token": "yyy"
    },
    "message": "Operation successful."
}
```
---

### POST `/auth/logout`

Revoke the `refresh_token` and ends the current session.

#### Headers
`Authorization: Bearer <refresh_token>`

#### Response
```json
{
    "message": "Operation successful."
}
```

---

### GET `/auth/me`

Validate the `access_token` and returns user ID.

#### Headers
`Authorization: Bearer <access_token>`

#### Response
```json
{
    "data": {
        "id": 1
    },
    "message": "Operation successful."
}
```
---

### GET `/auth/confirm/<token>`

Validate email token.

#### Response

Returns a HTML page **email_confirmed.html** or **email_error.html**

---

### POST `/auth/resend`

Resend email verification token.

#### Request
```json
{
    "email": "mail@domain.com"
}
```
#### Response
```json
{
    "message": "Operation successful."
}
```
---

### POST `/auth/callback/google`

Callback for Google authentication.

#### Request
```json
{
    "W.I.P"
}
```
#### Response
```json
{
    "W.I.P"
}
```
---

## Users

### GET `/users`

List all users (Admin only).

#### Headers
`Authorization: Bearer <access_token>`

#### Response
```json
{
    "data": [
        {
            "created_at": "2025-07-14T05:48:03",
            "email": "mail@domain.com",
            "id": 1,
            "name": "Real Name"
        },
        {
            "created_at": "2025-07-14T05:48:04",
            "email": "mail@domain.com",
            "id": 2,
            "name": "Real Name"
        }
    ],
    "message": "Operation successful."
}
```
---

### POST `/users/register`

Register a new user.

#### Headers
`Authorization: Bearer <access_token>`

#### Request
```json
{
    "name":"Real Name",
    "password":"pass",
    "email":"xyz@domain.com",
    "recaptcha_token":"token"
}
```
#### Response
```json
{
    "data": {
        "created_at": "2025-01-01T23:59:59",
        "email": "xyz@domain.com",
        "id": 1,
        "name": "Real Name"
    },
    "message": "Resource created successfully."
}
```
---

### GET `/users/<id>`

List a user (Admin or Owner only).

#### Headers
`Authorization: Bearer <access_token>`

#### Response
```json
{
    "data": {
        "created_at": "2025-07-14T05:48:04",
        "email": "mail@domain.com",
        "id": 1,
        "name": "Real Name",
    },
    "message": "Operation successful."
}
```
---
### PATCH `/users/<id>`

Update individual attributes of a user (Admin or Owner only).

#### Headers
`Authorization: Bearer <access_token>`

#### Request
```json
{
  "name": "New name"
}
```
#### Response
```json
{
    "data": {
            "created_at": "2025-07-14T05:48:04",
            "email": "mail@domain.com",
            "id": 1,
            "name": "New name"
    },
    "message": "Operation successful."
}
```
---
### DELETE `/users/<id>`

Deletes user (Admin only).

#### Headers
`Authorization: Bearer <access_token>`

#### Response
```json
{
    "message": "Operation successful."
}
```
---
