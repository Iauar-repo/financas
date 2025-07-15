from flask import request, jsonify, current_app as app
from flask_jwt_extended import jwt_required

from app.users.service import listUsers_, createUser_, updateUser_, deleteUser_
from app.users import users_bp
from app.auth.utils import admin_required, owner_or_admin_required
from app.extensions import limiter

# GET  /api/users  Listar usuários
@users_bp.get('/')
@jwt_required()
@admin_required
def listUsers():
    result, error, status = listUsers_()
    if error:
        return jsonify(message=error), status
    
    return jsonify(result), status

# POST  /api/users  Criar novo usuário
@users_bp.post('/registro')
@limiter.limit("2 per 5 minutes")
def createUser():
    input = request.get_json()
    
    result, error, status = createUser_(input)
    if error:
        return jsonify(message=error), status
    
    return jsonify(result), status

# GET  /api/users/<id>  Detalhes de um usuário
@users_bp.get('/<int:user_id>')
@jwt_required()
@owner_or_admin_required
def getUser(user_id):
    result, error, status = listUsers_(user_id)
    if error:
        return jsonify(message=error), status
    
    return jsonify(result), status

# PATCH  /api/users/<id>  Atualizar usuário
@users_bp.patch('/<int:user_id>')
@jwt_required()
@owner_or_admin_required
def updateUser(user_id):
    input = request.get_json()
    
    result, error, status = updateUser_(input, user_id)
    if error:
        return jsonify(message=error), status
    
    return jsonify(result), status

# DELETE  /api/users/<id>  Deletar usuário
@users_bp.delete('/<int:user_id>')
@jwt_required()
@admin_required
def deleteUser(user_id):
    result, error, status = deleteUser_(user_id)
    if error:
        return jsonify(message=error), status
    
    return jsonify(result), status
