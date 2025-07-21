from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jti,
    verify_jwt_in_request,
    get_jwt,
    get_jwt_identity
)
from functools import wraps
from app.core.responses import response
from itsdangerous import URLSafeTimedSerializer
from flask import current_app as app
from flask_mail import Message
from app.extensions import mail

def generate_tokens(user_id, is_admin):
    access = create_access_token(
        identity=str(user_id),
        additional_claims={"is_admin": is_admin}
    )
    refresh = create_refresh_token(
        identity=str(user_id),
        additional_claims={"is_admin": is_admin}
    )
    jti_acc = get_jti(access)
    jti_ref = get_jti(refresh)

    return access, refresh, jti_acc, jti_ref

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if not claims.get("is_admin"):
            return response("FORBIDDEN")
        return fn(*args, **kwargs)
    return wrapper

def owner_or_admin_required(fn):
    @wraps(fn)
    def wrapper(user_id, *args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        current_user_id = int(get_jwt_identity())

        if not claims.get("is_admin") and current_user_id != user_id:
            return response("FORBIDDEN")

        return fn(user_id, *args, **kwargs)
    return wrapper

def generate_confirmation_token(email):
    s = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    return s.dumps(email, salt="email-confirm")

def confirm_token(token, expiration=3600):
    s = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    try:
        email = s.loads(token, salt="email-confirm", max_age=expiration)
    except Exception:
        return None
    return email

def send_confirmation_email(user):
    token = generate_confirmation_token(user.email)
    confirm_url = f"http://localhost:5000/api/auth/confirm/{token}"
    html = f"<p>Olá {user.name}, confirme seu e-mail clicando <a href='{confirm_url}'>aqui</a>.</p>"

    msg = Message(subject="Confirme seu e-mail", recipients=[user.email], html=html)
    mail.send(msg)
