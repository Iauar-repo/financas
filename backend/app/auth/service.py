from flask_bcrypt import check_password_hash
from flask import current_app as app

from app.extensions import db
from app.models import Users, ActiveSessions, TokenBlocklist
from .utils import generate_tokens


# helper: cria nova sessão
def create_session(user_id: int, refresh_jti: str, ip: str):
    db.session.add(ActiveSessions(
        jti = refresh_jti,
        user_id = user_id,
        ip_address = ip
    ))

# helper: revoga sessão antiga
def revoke_old_session(user_id: int):
    old = ActiveSessions.query.filter_by(user_id = user_id).first()
    if old:
        db.session.add(TokenBlocklist(
            jti = old.jti,
            user_id = user_id,
            ip_address = old.ip_address,
            created_at = old.created_at,
            expires_at = old.expires_at
        ))
        db.session.delete(old)

# main: login
def login_user(username: str, password: str, ip_address: str):
    try:
        user = Users.query.filter_by(nickname=username).first()
        if not user:
            app.logger.error(f"[Login] Usuário não existe: {username}")
            return None, "Usuário não existe", 401

        if not check_password_hash(user.password, password):
            app.logger.error(f"[Login] Senha incorreta. User: {username}")
            return None, "Senha incorreta", 401

        revoke_old_session(user.id)
        access_token, refresh_token, _, refresh_jti = generate_tokens(user.id)
        create_session(user.id, refresh_jti, ip_address)
        db.session.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "message": "Usuário logado com sucesso"
        }, None, 200
    
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Erro desconhecido no Login: {str(e)}")
        return None, f"Erro desconhecido: {str(e)}", 500

# main: logout
def logout_user(user_id: int):
    try:
        revoke_old_session(user_id)
        db.session.commit()

        return {
            "message": "Usuário deslogado com sucesso"
        }, None, 200

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Erro desconhecido no Logout: {str(e)}")
        return None, f"Erro desconhecido: {str(e)}", 500

# main: gera novo refresh_token
def rotate_refresh_token(user_id: int, jti: str, ip_address: str):
    try:
        current_token = ActiveSessions.query.filter_by(jti=jti, user_id=user_id).first()

        if current_token.ip_address != ip_address:
            app.logger.error(f"[refresh token] IP não autorizado: {ip_address} | Esperado: {current_token.ip_address}")
            return None, "Endereço IP não autorizado", 403

        revoke_old_session(user_id)
        access_token, refresh_token, _, refresh_jti = generate_tokens(user_id)
        create_session(user_id, refresh_jti, ip_address)
        db.session.commit()

        return { 
            "access_token": access_token,
            "refresh_token": refresh_token,
            "message": "Novos tokens foram gerados"
            }, None, 200
    
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Erro desconhecido ao gerar novos tokens: {str(e)}")
        return None, f"Erro desconhecido: {str(e)}", 500

# main: checkagem de sessão
def whoami(user_id: int):
    try:
        user = Users.query.get(user_id)

        if not user:
            app.logger.error(f"[WhoamI] Usuário não existe. ID: {user_id}")
            return None, 'Usuário não existe', 404
        
        return {
            "id": user.id,
            "nickname": user.nickname,
            "message": 'Autenticado'
        }, None, 200
    
    except Exception as e:
        app.logger.error(f"Erro desconhecido ao buscar infos do usuário: {str(e)}")
        return None, f"Erro desconhecido: {str(e)}", 500
