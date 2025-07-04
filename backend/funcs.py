from app import app
from models import Users
from flask import request, session, jsonify
from flask_bcrypt import check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route('/api/test')
@jwt_required()
def index():
    user_id = int(get_jwt_identity())  # ID do usuário dentro do token
    user = Users.query.get(user_id)
    #users = Users.query.all()
    #for line in users:
        #print(line.id)
        #print(line.name)
        #print(line.nickname)
        #print(line.password)
    
    if not user:
        return jsonify(message="User not found"), 404

    return jsonify(id=user.id, nickname=user.nickname, message='Authenticated'), 200

