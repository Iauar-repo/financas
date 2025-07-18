from flask import request, jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from app.auth.service import (
    login_user,
    logout_user,
    rotate_refresh_token,
    whoami,
    confirmEmail_,
    reenvioEmail_
)
from app.auth import auth_bp

@auth_bp.get('/health')
def health():
    return jsonify(message="OK"), 200

@auth_bp.post('/login')
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    ip_address = request.remote_addr

    result, error, status = login_user(username, password, ip_address)
    if error:
        return jsonify(message=error), status
    
    return jsonify(result), status

@auth_bp.post("/logout")
@jwt_required(refresh=True)
def logout():
    user_id = int(get_jwt_identity())

    result, error, status = logout_user(user_id)
    if error:
        return jsonify(message=error), status
    
    return jsonify(result), status

@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    jti = get_jwt()["jti"]
    user_id = int(get_jwt_identity())
    ip_address = request.remote_addr

    result, error, status = rotate_refresh_token(user_id, jti, ip_address)
    if error:
        return jsonify(message=error), status
    
    return jsonify(result), status

@auth_bp.get('/me')
@jwt_required()
def me():
    user_id = int(get_jwt_identity())

    result, error, status = whoami(user_id)
    if error:
        return jsonify(message=error), status
    
    return jsonify(result), status

@auth_bp.get("/confirm/<token>")
def confirmEmail(token):
    error, status = confirmEmail_(token)
    if error:
        return render_template("email_error.html", error=error)
    
    return render_template("email_confirmed.html")

@auth_bp.post("/reenvio")
def reenvioEmail():
    data = request.get_json()
    email = data.get('email')

    result, error, status = reenvioEmail_(email)
    if error:
        return jsonify(message=error), status
    
    return jsonify(result), status
