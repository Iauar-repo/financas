## **Project status:** Work in Progress (this readme included)

A clean, secure API that lets users record incomes and expenses, manage profiles and authentication (email/password + Google OAuth), and later analyze their financial data.


[API Document](api.md) <br><br>

<details>
  <summary>⚙️ How to run</summary>

1. **Clone and install**

    ```bash 
    git clone https://github.com/Iauar-repo/financas.git
    cd financas/backend
    pip install -r requirements.txt
    ```

2. **Environment**

    Copy `.env.example` → `.env` and fill in:

    ```bash
    FLASK_APP=run.py
    DATABASE_URL=…
    JWT_SECRET_KEY=…
    REDIS_URL=…
    ```

3. **Database setup**
    ```bash
    flask db upgrade
    python init_database.py
    ```

4. **Run**

    ```bash
    flask run
    ```
</details>


# 🛠️ Tech Stack
- **Language & Framework:** Python 3.11, Flask
- **Auth & Security:** Flask‑JWT‑Extended, Flask‑Bcrypt, OAuth2 (Google)
- **Rate‑Limiting:** Flask‑Limiter with Redis backend
- **DB & Migrations:** MySQL, SQLAlchemy, Flask‑Migrate (Alembic)
- **Validation:** Marshmallow
- **Testing:** pytest
- **CI/CD:** GitHub Actions
- **Monitoring & Logging:** Python logging, rotating file handler

# 📐 Architecture: Application Factory + Blueprints

```
app/
├── __init__.py          # Create app object + JWT configuration
├── config.py            # Load .env and global variables
├── extensions.py        # Initiate instances
├── models.py            # Database models
├── auth/
│   ├── __init__.py      # Blueprint auth
│   ├── jwt_handlers.py  # JWT error handling
│   ├── repository.py    # Data access layer
│   ├── routes.py        # Endpoints
│   ├── schemas.py       # Payload validator
│   ├── service.py       # Business logic
|   ├── utils.py         # Generic helper functions
├── core
|   ├── responses.py     # Controller for text responses
├── users/
│   ├── __init__.py      # Blueprint users
│   ├── repository.py    # Data access layer
│   ├── routes.py        # Endpoints
│   ├── schemas.py       # Payload validator
│   ├── service.py       # Business logic
|   ├── utils.py         # Generic helper functions
```

# 🔒 Secutiry

- JWTs with short‑lived access tokens (15 min) and rotating refresh tokens (7 days).
- Passwords hashed with Bcrypt.
- OAuth2 integration for Google login.
- Rate‑limiting on sensitive endpoints backed by Redis.
- Referential cascade deletes on user removal (SQLAlchemy + DB‑level).

# ✅ Testing

- **pytest** suite covering auth flows, user endpoints, and error cases.
- In‑memory SQLite test DB, fixtures in `tests/`.
- **Coverage:** > 80% on core modules.

<br>

> By: [Rodrigo Lopes](https://github.com/rodrigofl-dev) — Backend developer and Data analyst.