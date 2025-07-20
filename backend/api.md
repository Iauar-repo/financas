# 📘 Documentação da API - Projeto Finanças

Detalhamento dos endpoints
<details>
  <summary>Autenticação</summary>

### POST `/api/auth/login`

Autentica o usuário com `username` e `password`.

#### Request
```json
{
    "username": "username",
    "password": "123"
}
```

#### Response
```json
{
    "access_token": "xxx",
    "refresh_token": "yyy",
    "message": "Usuário logado com sucesso"
}
```

---

### POST `/api/auth/refresh`

Gera novos tokens com base no `refresh_token`.

#### Headers
`Authorization: Bearer <refresh_token>`

#### Response
```json
{
    "access_token": "xxx",
    "refresh_token": "yyy",
    "message": "Novos tokens foram gerados"
}
```

---

### POST `/api/auth/logout`

Revoga o `refresh_token` e encerra a sessão.

#### Headers
`Authorization: Bearer <refresh_token>`

#### Response
```json
{
    "message": "Usuário deslogado com sucesso"
}
```

---

### GET `/api/auth/me`

Valida o `access_token` e retorna os dados do usuário autenticado.

#### Headers
`Authorization: Bearer <access_token>`

#### Response
```json
{
    "id": 1,
    "message": "Autenticado"
}
```
---

### GET `/api/auth/confirm/<token>`

Valida o token de confirmação de email.

#### Response

Retorna página HTML **email_confirmado.html** ou **email_error.html**

---

### POST `/api/auth/resend`

Reenvia token de verificação de email.

#### Request
```json
{
    "email": "mail@domain.com"
}
```
#### Response
```json
{
    "message": "Email de confirmação foi reenviado"
}
```
---
</details>

<details>
  <summary>Usuários</summary>

### POST `/api/users/register`

Cria um novo usuário.

#### Headers
`Authorization: Bearer <access_token>`

#### Request
```json
{
    "name":"Real Name",
    "username":"xyz",
    "password":"pass",
    "email":"xyz@domain.com",
    "recaptcha_token":"token"
}
```

#### Response
```json
{
    "message": "Usuário xyz registrado"
}
```

---

### GET `/api/users`

Lista todos os usuários (Admin only).

#### Headers
`Authorization: Bearer <access_token>`

#### Response
```json
{
  [
    {
        "created_at": "2025-07-14T05:48:03",
        "email": "mail@domain.com",
        "id": 1,
        "name": "Real Name",
        "username": "user1"
    },
    {
        "created_at": "2025-07-14T05:48:04",
        "email": "mail@domain.com",
        "id": 2,
        "name": "Real Name",
        "username": "user2"
    }
]
}
```
---

### GET `/api/users/<id>`

Lista um usuário específico (Admin or Owner only).

#### Headers
`Authorization: Bearer <access_token>`

#### Response
```json

{
    "created_at": "2025-07-14T05:48:04",
    "email": "mail@domain.com",
    "id": 1,
    "name": "Real Name",
    "username": "user1"
}
```

---

### PATCH `/api/users/<id>`

Atualiza dados do usuário especificado (Admin or Owner only).

#### Headers
`Authorization: Bearer <access_token>`

#### Request
```json
{
  "name": "Novo Nome"
}
```

#### Response
```json
{
    "created_at": "2025-07-14T05:48:04",
    "email": "mail@domain.com",
    "id": 1,
    "name": "Novo Nome",
    "username": "user1"
}
```
---

### DELETE `/api/users/<id>`

Remove o usuário especificado (Admin only).

#### Headers
`Authorization: Bearer <access_token>`

#### Response
```json
{
    "message": "Usuário user1 foi deletado"
}
```
---
</details>