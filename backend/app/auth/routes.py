from flask import request, render_template, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from app.extensions import oauth
from app.core.responses import response
from app.auth import auth_bp
from .service import (
    login_,
    logout_,
    refresh_tokens_,
    me_,
    confirm_email_,
    resend_email_,
    callback_google_
)

# POST  /api/auth/login  Login
@auth_bp.post('/login')
def login():
    data = request.get_json()
    ip = request.remote_addr
    key,data = login_(data, ip)

    return response(key,data)

# POST  /api/auth/logout  Logout
@auth_bp.post("/logout")
@jwt_required(refresh=True)
def logout():
    user_id = int(get_jwt_identity())
    key,data = logout_(user_id)

    return response(key,data)

# POST  /api/auth/refresh  Refresh tokens
@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh_tokens():
    refresh_jti = get_jwt()["jti"]
    user_id = int(get_jwt_identity())
    ip = request.remote_addr
    key,data = refresh_tokens_(refresh_jti, user_id, ip)

    return response(key,data)

# GET  /api/auth/me  Check user authentication
@auth_bp.get('/me')
@jwt_required()
def me():
    user_id = int(get_jwt_identity())
    key,data = me_(user_id)

    return response(key,data)

# GET  /api/auth/confirm/<token>  Confirm email registration by token
@auth_bp.get("/confirm/<token>")
def confirm_email(token):
    error = confirm_email_(token)
    if error:
        return render_template("email_error.html", error=error)
    
    return render_template("email_confirmed.html")

# GET  /api/auth/resend  Resend email confirmation
@auth_bp.post("/resend")
def resend_email():
    data = request.get_json()
    email = data.get('email')
    key,data = resend_email_(email)

    return response(key,data)

# GET  /api/auth/login/google  OAuth2.0 # MOVER PARA O FRONT
@auth_bp.get('/login/google')
def login_google():
    redirect_uri = url_for('auth.callback_google', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

# GET  /api/auth/callback/google  OAuth2.0 Callback
@auth_bp.get('/callback/google')
def callback_google():
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.get('userinfo').json()
    ip = request.remote_addr
    key,data = callback_google_(user_info, ip)

    return response(key,data)
