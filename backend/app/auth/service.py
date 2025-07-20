from flask_bcrypt import check_password_hash
from flask import current_app as app
from app.extensions import db
from app.models import Users, ActiveSessions, TokenBlocklist
from app.auth.utils import generate_tokens, confirm_token, send_confirmation_email

# helper: insert new user | OAuth2
def _insertUser(input):
    db.session.add(Users(
        name = input.get('name'),
        email = input.get('email'),
        auth_provider = input.get('auth_provider')
    ))

# helper: create a new session
def _createSession(user_id, refresh_jti, ip):
    db.session.add(ActiveSessions(
        jti = refresh_jti,
        user_id = user_id,
        ip_address = ip
    ))

# helper: revoke the old session
def _revokeOldSession(user_id, session):
    db.session.add(TokenBlocklist(
        jti = session.jti,
        user_id = user_id,
        ip_address = session.ip_address,
        created_at = session.created_at,
        expires_at = session.expires_at
    ))
    db.session.delete(session)

# main: login
def login_(data, ip):
    try:
        username = data.get('username')
        password = data.get('password')
        user = Users.query.filter_by(username=username).first()
        if not user:
            app.logger.error(f"[Login] User not found: {username}")
            return "LOGIN_FAILED", None

        if not check_password_hash(user.password, password):
            app.logger.error(f"[Login] Wrong password. User: {username}")
            return "LOGIN_FAILED", None
        
        if not user.email_confirmed == 1:
            app.logger.error(f"[Login] Email not verified: {user.email}")
            return "FORBIDDEN", None
        
        if not user.auth_provider == "email":
            app.logger.error(f"[Login] User not found: {username}")
            return "LOGIN_FAILED", None

        is_admin = True if user.is_admin == 1 else False
        
        session = ActiveSessions.query.filter_by(user_id = user.id).first()
        if session:
            _revokeOldSession(user.id, session)
        
        access_token, refresh_token, _, refresh_jti = generate_tokens(user.id, is_admin)
        _createSession(user.id, refresh_jti, ip)
        db.session.commit()

        return "SUCCESS", {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"[Login] Internal error: {str(e)}")
        return "SERVER_ERROR", {"error":str(e)}

# main: logout
def logout_(user_id):
    try:
        session = ActiveSessions.query.filter_by(user_id = user_id).first()
        if not session:
            app.logger.error(f"[Logout] User not found. ID: {user_id} - THIS SHOULD NEVER HAPPEN")
            return "USER_NOT_FOUND", None
        
        _revokeOldSession(user_id, session)
        db.session.commit()

        return "SUCCESS", None

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"[Logout] Internal error: {str(e)}")
        return "SERVER_ERROR", {"error":str(e)}

# main: make new tokens
def refreshTokens_(jti, user_id, ip):
    try:
        session = ActiveSessions.query.filter_by(jti=jti, user_id=user_id).first()
        if not session:
            app.logger.error(f"[Refresh Token] User not found. ID: {user_id}")
            return "USER_NOT_FOUND", None

        if session.ip_address != ip:
            app.logger.error(f"[Refresh Token] IP address not authorized: {ip} | Expected: {session.ip_address}")
            return "UNAUTHENTICATED", None
        
        user = Users.query.filter_by(id=user_id).first()
        is_admin = True if user.is_admin == 1 else False

        _revokeOldSession(user_id, session)
        access_token, refresh_token, _, refresh_jti = generate_tokens(user_id, is_admin)
        _createSession(user_id, refresh_jti, ip)
        db.session.commit()

        return "SUCCESS", { 
            "access_token": access_token,
            "refresh_token": refresh_token
            }
    
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"[Refresh Token] Internal error: {str(e)}")
        return "SERVER_ERROR", {"error":str(e)}

# main: ping session
def me_(user_id):
    try:
        user = Users.query.get(user_id)

        if not user:
            app.logger.error(f"[WhoamI] User not found. ID: {user_id}")
            return "USER_NOT_FOUND", None
        
        return "SUCCESS", {
            "id": user.id
        }
    
    except Exception as e:
        app.logger.error(f"[WhoamI] Internal error: {str(e)}")
        return "SERVER_ERROR", {"error":str(e)}

# main: email confirmation
def confirmEmail_(token):
    try:
        email = confirm_token(token)
        if not email:
            app.logger.error(f"[ConfirmEmail] Invalid token or expired")
            return 'Token inválido ou expirado'

        user = Users.query.filter_by(email=email).first()
        if not user:
            app.logger.error(f"[ConfirmEmail] User not found. Email: {email}")
            return 'Usuário não existe'

        user.email_confirmed = 1
        db.session.commit()

        return None
    
    except Exception as e:
        app.logger.error(f"[ConfirmEmail] Internal error: {str(e)}")
        return f"Erro desconhecido: {str(e)}"

# main: resend email confirmation
def resendEmail_(email):
    try:
        user = Users.query.filter_by(email=email).first()
        if not user:
            app.logger.error(f"[ResendEmail] Email not registered: {email}")
            return "USER_NOT_FOUND", None
        
        if user.email_confirmed == 1:
            return "USER_ALREADY_EXISTS", None
        
        send_confirmation_email(user)

        return "SUCCESS", None

    except Exception as e:
        app.logger.error(f"[ResendEmail] Internal error: {str(e)}")
        return "SERVER_ERROR", {"error":str(e)}

# main: callback for Google login
def callbackGoogle_(user_info, ip):
    # user_info => {'email':'','family_name':'','given_name':'','id':'','name':'','picture':'','verified_email':''}
    try:
        email = user_info.get("email")
        
        check = Users.query.filter_by(email=email).first()
        if not check:
            data = {
                "name":user_info.get("name"),
                "email":email,
                "auth_provider":"google",
                "email_confirmed":1
            }
            _insertUser(data)
            db.session.commit()
        
        user = Users.query.filter_by(email=email).first()
        is_admin = True if user.is_admin == 1 else False
        
        session = ActiveSessions.query.filter_by(user_id = user.id).first()
        if session:
            _revokeOldSession(user.id, session)
        
        access_token, refresh_token, _, refresh_jti = generate_tokens(user.id, is_admin)
        _createSession(user.id, refresh_jti, ip)
        db.session.commit()

        return "SUCCESS", {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    
    except Exception as e:
        app.logger.error(f"[CallbackGOOGLE] Internal error: {str(e)}")
        return "SERVER_ERROR", {"error":str(e)}