from app.extensions import db
from app.models import AuthProvider, Users
from flask_bcrypt import generate_password_hash


def get_user_by_email(email: str):
    return Users.query.filter_by(email=email).first()


def get_user_by_id(id: int):
    return Users.query.filter_by(id=id).first()


def insert_user(data: dict):
    db.session.add(Users(name=data.get("name"), email=data.get("email")))


def insert_provider(
    user_id: int, provider: str, provider_id: str, password: str = None
):
    if provider == "email":
        db.session.add(
            AuthProvider(
                user_id=user_id,
                provider=provider,
                provider_user_id=provider_id,
                password_hash=generate_password_hash(password).decode("utf-8"),
            )
        )
    else:
        db.session.add(
            AuthProvider(
                user_id=user_id, provider=provider, provider_user_id=provider_id
            )
        )


def update_user(data: dict, user: Users):
    blacklist = ["id", "is_admin", "email_confirmed", "email"]
    for key, val in data.items():
        if key.lower() not in blacklist:
            setattr(user, key, val)


def get_all_users():
    return Users.query.all()
