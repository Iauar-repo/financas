from app import app
from models import Users
from flask import request, session, jsonify
from flask_bcrypt import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

@app.post('/api/login')
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    user = Users.query.filter_by(nickname=username).first()
    
    if not user:
        return jsonify(message='User not found'), 404
    
    if not check_password_hash(user.password, password):
        return jsonify(message='Wrong password'), 401
    
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify(token=access_token, message='User Logged in'), 200

@app.get('/api/validate')
@jwt_required()
def validate():
    user_id = int(get_jwt_identity())
    user = Users.query.get(user_id)

    if not user:
        return jsonify(message="Invalid Token"), 404

    return jsonify(id=user.id, nickname=user.nickname, message='Authenticated'), 200
