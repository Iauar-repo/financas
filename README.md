# 💰 Controle Financeiro Pessoal — App mobile

**Projeto desenvolvido por:**
- [Rafael Rondon](https://github.com/Rath09) — Front-end mobile
- [Rodrigo Lopes](https://github.com/rodrigofl-dev) — Back-end

<!-- GIF: grave uma demo curta do app e salve em docs/img/demo.gif -->
<p align="center">
  <img src="docs/img/demo.gif" alt="Demonstração do app" width="280" />
</p>

## 📌 Visão geral

App mobile de finanças pessoais. A visão do produto é registrar receitas e despesas,
gerar relatórios e acompanhar tudo em um dashboard — tendo autenticação segura como base.
O que já foi construído está descrito no **Escopo da v1** abaixo.

## ✅ Escopo da v1

O que está **implementado de fato** nesta versão:

**Autenticação (ponta a ponta)**
- Registro de usuário e login com JWT (access + refresh), com refresh automático em respostas `401`
- Logout com revogação de token (blacklist) e confirmação de e-mail (confirmar / reenviar)
- Sessão persistida com tokens no **Expo Secure Store**; estado global via Context API e rotas privadas protegidas
- Proteção anti-bot (reCAPTCHA) e rate limiting no back-end

**Perfil**
- Ver e editar o próprio perfil (nome / e-mail) via `GET /api/auth/me` + `PATCH /api/users/:id`

**Back-end**
- API Flask + MySQL com JWT, CRUD de usuários e migrações (Alembic)

### 🚧 Fora da v1 (ainda não implementado)

- **Transações (receitas/despesas):** a tela é um placeholder e não há endpoints no back-end
- **Gráficos / relatórios / dashboard:** telas placeholder, sem dados reais
- **Recuperação de senha:** o fluxo no app é apenas simulado (sem endpoint de reset no back-end)
- **Login com Google:** a rota de callback existe no back-end, mas ainda não está ligada no app

## 🙋 Minha contribuição

Front-end mobile (a camada que construí):

- **React Native + TypeScript** com **Expo Router** (navegação stack/tabs)
- Estado global de autenticação com **Context API** e hooks customizados
- **Autenticação JWT** ponta a ponta no cliente: login / refresh / logout, header
  `Authorization: Bearer <token>` e retry automático quando o access token expira (`401`)
- Tokens guardados com **Expo Secure Store** e telas privadas protegidas por guarda de rota

## 🔗 Acesso rápido

| Seção | Descrição | Link |
|-------|-----------|------|
| 🖥️ Frontend | React Native + TypeScript (Expo) | [Ver detalhes](frontend/readme.md) |
| 📡 Backend | API Flask + JWT | [Ver detalhes](backend/README.md) |

## 🛠️ Stack

<p align="left">
  <img src="https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/React_Native-20232A?logo=react&logoColor=61DAFB" alt="React Native" />
  <img src="https://img.shields.io/badge/Expo-000020?logo=expo&logoColor=white" alt="Expo" />
  <img src="https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=white" alt="MySQL" />
  <img src="https://img.shields.io/badge/JWT-000000?logo=jsonwebtokens&logoColor=white" alt="JWT" />
</p>

## 📄 Licença

[MIT](LICENSE).
