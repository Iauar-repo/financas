# Iauar Project – Frontend App (Expo React Native)

Este é o frontend **mobile** do Iauar Project, desenvolvido com **React Native** (Expo) e **TypeScript**, integrado a um backend Flask seguro via JWT.  
A aplicação foi projetada para ser modular, segura, fácil de manter, e moderna — com foco em usabilidade e boas práticas de autenticação.

---

## 🚀 Tecnologias utilizadas

- [React Native (Expo)](https://reactnative.dev/)
- TypeScript
- Expo Secure Store (armazenamento seguro de tokens)
- Expo Router (navegação stack/tabs)
- Context API e Hooks customizados (controle global de autenticação)
- REST API integration (backend Flask JWT)
- ESLint + Prettier (padrão de código)
- Styled Components (ou StyleSheet do RN)
- Modularização de serviços, hooks e utilitários

---

## 📁 Estrutura de diretórios

app/
├── (auth)/ # Telas públicas: login, register, forgot password
│ ├── login.tsx
│ ├── register.tsx
│ └── forgot-password.tsx
├── (tabs)/ # Telas privadas (protegidas por autenticação)
│ ├── index.tsx # Dashboard principal
│ ├── profile.tsx # Tela de perfil do usuário (edição via modal)
│ ├── transactions.tsx
│ ├── charts.tsx
│ └── debug.tsx # Tela de debug de autenticação/tokens
├── _layout.tsx # Root Layout (Provider de Auth)
├── components/ # Componentes reutilizáveis (botões, inputs, etc.)
├── constants/ # Constantes globais (cores, config)
├── services/ # Serviços de API: userService, authService, tokenService, api
├── hooks/ # Hooks customizados: useAuth, useColorScheme, etc.
├── utils/ # Helpers/utilitários: formatters, validation
└── assets/ # Imagens, ícones (profile-placeholder, etc.)

---

## 🔒 Fluxo de Autenticação JWT

<details>
  <summary>Detalhes do fluxo de autenticação</summary>

  - Contexto global de autenticação com React Context + Hooks
  - Tokens armazenados de forma segura (Expo Secure Store)
  - Login, logout, e refresh automáticos (com controle de sessão)
  - Proteção total das rotas (telas em `(tabs)` só acessíveis autenticado)
  - Busca de id do usuário via `/api/auth/me` (sempre autenticado)
  - Consulta e edição de dados completos via `/api/users/:id` (com token)
  - Edição de perfil feita via PATCH `/api/users/:id`, seguindo boas práticas REST
  - Headers `Authorization: Bearer <access_token>` em todas requisições protegidas
  - Tela de debug mostra tokens (mascarados), expiração, perfil, simulação de login/logout, e limpeza de credenciais
  - UI moderna, responsiva e acessível (placeholders, feedback visual, modais, etc.)
</details>

---

## 💡 Funcionalidades principais

- Login seguro (com validação e feedback de erros)
- Registro de novo usuário
- Recuperação de senha (simulada)
- Dashboard principal (após login)
- Visualização e edição de perfil completo (nome, email, etc.)
- Listagem de transações e gráficos (placeholders)
- Tela de debug para QA/desenvolvimento

---

## 🛠️ Scripts principais

- `npm start` — inicia o app em modo de desenvolvimento (Expo Go)
- `npm run lint` — checa padrão de código com ESLint
- `npm run build` — build de produção (quando aplicável)

---

## ✨ Padrões e boas práticas

- Tokens nunca expostos em tela (mascarados na debug)
- Não há duplicação de serviços (um único `userService`)
- Nenhum userId salvo localmente — sempre obtido via `/me` para máxima segurança
- Tipagem forte com TypeScript em todos serviços e componentes
- Separação de lógica de negócio, UI e utilitários
- Código modular, fácil de manter e expandir
- Responsivo em qualquer aparelho

---

## 🔗 Integração com Backend

- **Necessário backend compatível (Flask JWT ou similar)**
- Todas chamadas seguras usam o header:  
  `Authorization: Bearer <access_token>`
- Endpoints usados:
    - `/api/auth/login` (login)
    - `/api/auth/me` (busca id/nickname/autenticação)
    - `/api/auth/refresh` (refresh de tokens)
    - `/api/auth/logout` (logout/revoga sessão)
    - `/api/users/:id` (busca/edição completa do perfil do usuário)

---

## 🤝 Contribuindo

Sinta-se à vontade para abrir issues, sugerir melhorias ou enviar PRs!

---

> Feito por [Seu Nome] — Frontend mobile & UX.

---

