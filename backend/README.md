# Flask JWT Auth API – Backend de Autenticação Segura

Este é um backend construído com **Flask**, focado em autenticação segura usando **JWT (JSON Web Tokens)**, **controle de sessões**, **refresh tokens** e **boas práticas de segurança RESTful**.

O projeto foi estruturado com foco em **escalabilidade**, **manutenibilidade**, **separação de responsabilidades**, e é ideal para APIs modernas que exigem controle de login, proteção de rotas, gerenciamento de tokens e auditoria de sessão.

---

## 🚀 Tecnologias utilizadas

- Python 3.12+
- Flask
- Flask-JWT-Extended
- Flask-Bcrypt
- Flask-SQLAlchemy
- Flask-CORS
- MySQL 8+
- RESTful API
- JWT com blacklist
- Log com `logging + RotatingFileHandler`

---

## Estrutura de diretórios

```
app/
├── __init__.py          # Criação da app + configuração JWT
├── config.py            # Carrega variáveis do .env e varáveis globais
├── extensions.py        # Inicializa db, jwt, cors, etc
├── models.py            # Models: Users, ActiveSessions, TokenBlocklist, ...
├── auth/
│   ├── __init__.py      # Blueprint auth
│   ├── routes.py        # Endpoints /login, /logout, /refresh
│   ├── service.py       # Lógica de autenticação (login, sessões, rotação)
│   ├── jwt_handlers.py  # Tratamento de erros JWT
|   ├── utils.py         # Funções utilitárias
```

<details>
  <summary>Sistema de Login</summary>

  ### ✅ Autenticação JWT
  - Geração de `access_token` e `refresh_token`
  - Tokens são assinados e têm validade configurável via `config.py`

  ### ✅ Sessão única por usuário
  - Ao logar, sessões antigas são automaticamente revogadas
  - A nova sessão é armazenada com o `refresh_token` (via `ActiveSessions`)

  ### ✅ Refresh Token seguro
  - Refresh é atrelado ao IP de origem
  - Validade de rotação verificada no banco (IP match)

  ### ✅ Logout com blacklist
  - O token usado no logout (refresh) é movido para a tabela `TokenBlocklist`
  - Todos os tokens em blacklist são bloqueados automaticamente em qualquer rota protegida

  ### ✅ Proteção de rotas com `@jwt_required()`
  - Se token for revogado, inválido, ausente ou expirado → retorna erro personalizado

  ### ✅ Validação e tratamento de erros
  - Todos os erros JWT têm tratamento:
  - `expired_token_loader`
  - `invalid_token_loader`
  - `unauthorized_loader`
  - `revoked_token_loader`
  - Retorno estruturado em JSON + log da falha no `app.log`

  ### ✅ Padrões RESTful
  - `POST /auth/login` – autenticação
  - `POST /auth/refresh` – gera novo access token
  - `POST /auth/logout` – encerra sessão (revoga refresh)
  - `GET /auth/me` – valida token atual e retorna infos do usuário da sessão

  ---
</details>

## Em desenvolvimento
### Autenticação e Login:
- Testes automatizados com Pytest
- OAuth 2.0 / login social
- Autenticação por digitais
- Rate limiting e brute-force protection

### Usuários - CRUD
- Criação/registro de usuários
- Consulta de usuários registrados
- Atualização de cadastro/perfil
- Remoção/exclusão de usuários

> Feito por [Rodrigo Lopes](https://github.com/rodrigofl-dev) — Backend e análise de dados.