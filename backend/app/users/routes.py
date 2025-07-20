from flask import request, jsonify
from flask_jwt_extended import jwt_required

from app.users.service import listUsers_, createUser_, updateUser_, deleteUser_
from app.users import users_bp
from app.auth.utils import admin_required, owner_or_admin_required
from app.extensions import limiter, oauth
from app.core.responses import response

# GET  /api/users  List users
@users_bp.get('/')
@jwt_required()
@admin_required
def listUsers():
    key,data = listUsers_()

    return response(key,data if data else None)

# POST  /api/users/register  Create a new user
@users_bp.post('/register')
@limiter.limit("2 per 5 minutes")
def createUser():
    key,data = createUser_(request.get_json())

    return response(key,data if data else None)

# GET  /api/users/<id>  List a user
@users_bp.get('/<int:user_id>')
@jwt_required()
@owner_or_admin_required
def getUser(user_id):
    key,data = listUsers_(user_id)
    
    return response(key,data if data else None)

# PATCH  /api/users/<id>  Update a user
@users_bp.patch('/<int:user_id>')
@jwt_required()
@owner_or_admin_required
def updateUser(user_id):
    key,data = updateUser_(request.get_json(), user_id)
    
    return response(key,data if data else None)

# DELETE  /api/users/<id>  Deletar usuário
@users_bp.delete('/<int:user_id>')
@jwt_required()
@admin_required
def deleteUser(user_id):
    key,data = deleteUser_(user_id)
    
    return response(key,data if data else None)

# GET  /api/users/callback/google  OAuth2.0 Callback
@users_bp.get('/callback/google')
def callbackGoogle():
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.get('userinfo').json()
    # user_info => {'email':'','family_name':'','given_name':'','id':'','name':'','picture':'','verified_email':''}

    #user = get_or_create_user_by_email(user_info['email'])

    #jwt_token = create_jwt_token(user_id=user.id)

    return jsonify({'dados': user_info, 'token':token})
