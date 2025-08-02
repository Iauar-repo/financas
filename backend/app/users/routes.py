from app.auth.utils import admin_required, owner_or_admin_required
from app.core.responses import response
from app.extensions import limiter
from app.users import users_bp
from app.users.service import create_user_, delete_user_, list_users_, update_user_
from flask import request
from flask_jwt_extended import jwt_required


# GET  /api/users  List users
@users_bp.get("/")
@jwt_required()
@admin_required
def list_users():
    key, data = list_users_()

    return response(key, data if data else None)


# POST  /api/users/register  Create a new user
@users_bp.post("/register")
# @limiter.limit("2 per 5 minutes")
def create_user():
    key, data = create_user_(request.get_json())

    return response(key, data if data else None)


# GET  /api/users/<id>  List a user
@users_bp.get("/<int:user_id>")
@jwt_required()
@owner_or_admin_required
def get_user(user_id):
    key, data = list_users_(user_id)

    return response(key, data if data else None)


# PATCH  /api/users/<id>  Update a user
@users_bp.patch("/<int:user_id>")
@jwt_required()
@owner_or_admin_required
def update_user(user_id):
    key, data = update_user_(request.get_json(), user_id)

    return response(key, data if data else None)


# DELETE  /api/users/<id>  Deletar usuário
@users_bp.delete("/<int:user_id>")
@jwt_required()
@admin_required
def delete_user(user_id):
    key, data = delete_user_(user_id)

    return response(key, data if data else None)
