from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.extensions import db
from app.models import Users, ActiveSessions

api_bp = Blueprint('api', __name__)

@api_bp.route('/ping')
@jwt_required()
def ping():
    user_id = int(get_jwt_identity())  # ID do usuário dentro do token
    user = Users.query.get(user_id)
    jti = get_jwt()["jti"]
    
    if not user:
        return jsonify(message="User not found"), 404
    
    session = ActiveSessions.query.filter_by(user_id=user.id).first()

    return jsonify(id=user.id, nickname=user.nickname, jti=jti, jti_session=session.jti, message='Authenticated'), 200
