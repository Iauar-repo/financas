from flask_bcrypt import check_password_hash
from flask import current_app as app

from app.extensions import db
from app.models import Users, ActiveSessions, TokenBlocklist
from app.auth.utils import generate_tokens, confirm_token, send_confirmation_email


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
        user = Users.query.filter_by(username=username).first()
        if not user:
            app.logger.error(f"[Login] Usuário não existe: {username}")
            return None, "Usuário não existe", 404

        if not check_password_hash(user.password, password):
            app.logger.error(f"[Login] Senha incorreta. User: {username}")
            return None, "Senha incorreta", 404
        
        if not user.email_confirmed == 1:
            app.logger.error(f"[Login] Email não verificado: {user.email}")
            return None, "Email não verificado", 404

        is_admin = True if user.is_admin == 1 else False
        
        revoke_old_session(user.id)
        access_token, refresh_token, _, refresh_jti = generate_tokens(user.id, is_admin)
        create_session(user.id, refresh_jti, ip_address)
        db.session.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "message": "Usuário logado com sucesso"
        }, None, 200
    
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"[Login] Erro desconhecido no Login: {str(e)}")
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
        app.logger.error(f"[Logout] Erro desconhecido no Logout: {str(e)}")
        return None, f"Erro desconhecido: {str(e)}", 500

# main: gera novo refresh_token
def rotate_refresh_token(user_id: int, jti: str, ip_address: str):
    try:
        current_token = ActiveSessions.query.filter_by(jti=jti, user_id=user_id).first()

        if current_token.ip_address != ip_address:
            app.logger.error(f"[refresh token] IP não autorizado: {ip_address} | Esperado: {current_token.ip_address}")
            return None, "Endereço IP não autorizado", 403

        user = Users.query.filter_by(id=user_id).first()
        is_admin = True if user.is_admin == 1 else False

        revoke_old_session(user_id)
        access_token, refresh_token, _, refresh_jti = generate_tokens(user_id, is_admin)
        create_session(user_id, refresh_jti, ip_address)
        db.session.commit()

        return { 
            "access_token": access_token,
            "refresh_token": refresh_token,
            "message": "Novos tokens foram gerados"
            }, None, 200
    
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"[refresh token] Erro desconhecido ao gerar novos tokens: {str(e)}")
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
            "nickname": user.username,
            "message": 'Autenticado'
        }, None, 200
    
    except Exception as e:
        app.logger.error(f"[WhoamI] Erro desconhecido ao buscar infos do usuário: {str(e)}")
        return None, f"Erro desconhecido: {str(e)}", 500

# main: confirmação de email
def confirmEmail_(token):
    try:
        email = confirm_token(token)
        if not email:
            app.logger.error(f"[ConfirmEmail] Token inválido ou expirado")
            return None, 'Token inválido ou expirado', 404

        user = Users.query.filter_by(email=email).first()
        if not user:
            app.logger.error(f"[ConfirmEmail] Usuário não existe. Email: {email}")
            return None, 'Usuário não existe', 404

        user.email_confirmed = 1
        db.session.commit()

        return {"message":"Email confirmado com sucesso"}, None, 200
    
    except Exception as e:
        app.logger.error(f"[ConfirmEmail] Erro desconhecido ao confirmar email: {str(e)}")
        return None, f"Erro desconhecido: {str(e)}", 500

# main: reenvio confirmação de email
def reenvioEmail_(email):
    try:
        user = Users.query.filter_by(email=email).first()
        if not user:
            app.logger.error(f"[ReenvioEmail] Email não registrado: {email}")
            return None, 'Email não registrado', 404
        
        if user.email_confirmed == 1:
            return {"message":"Email já confirmado"}, None, 200
        
        send_confirmation_email(user)

        return {"message":"Email de confirmação foi reenviado"}, None, 200

    except Exception as e:
        app.logger.error(f"[ReenvioEmail] Erro desconhecido ao reenviar email: {str(e)}")
        return None, f"Erro desconhecido: {str(e)}", 500
