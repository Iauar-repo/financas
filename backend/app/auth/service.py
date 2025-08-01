from flask_bcrypt import check_password_hash
from flask import current_app as app
from marshmallow import ValidationError

from app.extensions import db
from app.users.repository import (
    get_user_by_email,
    get_user_by_id,
    insert_user,
    insert_provider
)

from .utils import generate_tokens, confirm_token, send_confirmation_email
from .schemas import login_schema, create_user_social_schema
from .repository import (
    create_session,
    get_user_by_provider,
    get_active_session,
    get_session_by_jti,
    revoke_session
)

def login_(input: dict, ip: str):
    """
    Handle authentication login

    Parameters:
        input (dict): JSON payload with fields: email, password.
        ip (str): IP Address requesting login.

    Returns:
        tuple: (status: str, data: dict)
    """
    try:
        data = login_schema.load(input)
        user, ap = get_user_by_provider('email', data['email'])
        if not user:
            app.logger.error(f"[Login] User not found: {data['email']}")
            return "LOGIN_FAILED", None
        
        if not check_password_hash(ap.password_hash, data['password']):
            app.logger.error(f"[Login] Wrong password. User: {user.email}")
            return "LOGIN_FAILED", None
        
        if not user.email_confirmed:
            app.logger.error(f"[Login] Email not verified: {user.email}")
            return "FORBIDDEN", None

        is_admin = bool(user.is_admin)

        session = get_active_session(user.id)
        if session:
            revoke_session(user.id, session)

        access_token, refresh_token, _, refresh_jti = generate_tokens(user.id, is_admin)
        create_session(user.id, refresh_jti, ip)
        db.session.commit()

        return "SUCCESS", {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    
    except ValidationError as e:
        app.logger.error(f"[Login] Invalid payload: {str(e.messages)}")
        return "INVALID_PAYLOAD", {"error":str(e.messages)}

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"[Login] Internal error: {str(e)}")
        return "SERVER_ERROR", None

def logout_(user_id: int):
    """
    Handle authentication logout

    Parameters:
        user_id (int): User ID to log out.

    Returns:
        tuple: (status: str, None)
    """
    try:
        session = get_active_session(user_id)
        if session:
            revoke_session(user_id, session)
            db.session.commit()

        return "SUCCESS", None

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"[Logout] Internal error: {str(e)}")
        return "SERVER_ERROR", None

def refresh_tokens_(refresh_jti: str, user_id: int, ip: str):
    """
    Rotate access and refresh tokens

    Parameters:
        refresh_jti (str): Unique identifier (JTI) of the refresh token.
        user_id (int): User ID.
        ip (str): IP address from which the session is created.

    Returns:
        tuple: (status: str, data: dict)
    """
    try:
        session = get_session_by_jti(refresh_jti, user_id)
        if session.ip_address != ip:
            app.logger.error(f"[Refresh Token] IP address not authorized: {ip} | Expected: {session.ip_address}")
            return "UNAUTHENTICATED", None
        
        user = get_user_by_id(user_id)
        if not user:
            app.logger.error(f"[Refresh Token] No active sessions. User ID: {user_id}")
            return "USER_NOT_FOUND", None
        
        is_admin = bool(user.is_admin)
        revoke_session(user_id, session)
        access_token, refresh_token, _, refresh_jti = generate_tokens(user_id, is_admin)
        create_session(user_id, refresh_jti, ip)
        db.session.commit()

        return "SUCCESS", { 
            "access_token": access_token,
            "refresh_token": refresh_token
            }

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"[Refresh Token] Internal error: {str(e)}")
        return "SERVER_ERROR", None

def me_(user_id: int):
    """
    Check user authentication - Ping

    Parameters:
        user_id (int): User ID.

    Returns:
        tuple: (status: str, data: dict)
    """
    try:
        user = get_user_by_id(user_id)
        if not user:
            app.logger.error(f"[WhoamI] User not found: {user_id}")
            return "USER_NOT_FOUND", None
        
        return "SUCCESS", {
            "id": user.id
        }
    
    except Exception as e:
        app.logger.error(f"[WhoamI] Internal error: {str(e)}")
        return "SERVER_ERROR", None

def confirm_email_(token: str):
    """
    Send an email with a confirmation link

    Parameters:
        token (str): itsdangerous's token, generated during user registration
    
    Returns:
        HTML template.
    """
    try:
        email = confirm_token(token)
        if not email:
            app.logger.error(f"[ConfirmEmail] Invalid token or expired")
            return 'Parece que este link já expirou :('

        user = get_user_by_email(email)
        if not user:
            app.logger.error(f"[ConfirmEmail] User not found: {email}")
            return 'E-mail não registrado! Tente novamente ou entre em contato com a equipe de suporte.'
        
        user.email_confirmed = 1
        db.session.commit()

        return None        

    except Exception as e:
        app.logger.error(f"[ConfirmEmail] Internal error: {str(e)}")
        return f"Erro desconhecido. Favor entrar em contato com a equipe de suporte."

def resend_email_(email: str):
    """
    Resend the email with a confirmation link

    Parameters:
        email (str): Email that will receive the link
    
    Returns:
        tuple: (status: str, None)
    """
    try:
        user = get_user_by_email(email)
        if not user:
            app.logger.error(f"[ResendEmail] User not found: {email}")
            return "USER_NOT_FOUND", None
        
        if user.email_confirmed:
            return "USER_ALREADY_EXISTS", {
                "message":"Email already confirmed"
            }
        
        send_confirmation_email(user)
        return "SUCCESS", None        
    
    except Exception as e:
        app.logger.error(f"[ResendEmail] Internal error: {str(e)}")
        return "SERVER_ERROR", None

def callback_google_(user_info: dict, ip: str):
    """
    Callback OAuth2 from Google

    Parameters:
        user_info (dict): Google information of the user.
        ip (str): IP Address of the user.
    
    Returns:
        tuple: (status: str, data: dict)
    """
    try:
        data = create_user_social_schema.load(user_info)
        provider = 'google'
        user, _ = get_user_by_provider(provider, data['id'])

        if not user:
            user = get_user_by_email(data['email'])
            if not user:
                insert_user(data)
                db.session.flush()
                user = get_user_by_email(data['email'])

            if not user.email_confirmed:
                user.email_confirmed = 1
            
            insert_provider(user.id,provider,data['id'])
            db.session.commit()
        
        is_admin = bool(user.is_admin)

        session = get_active_session(user.id)
        if session:
            revoke_session(user.id, session)
        
        access_token, refresh_token, _, refresh_jti = generate_tokens(user.id, is_admin)
        create_session(user.id, refresh_jti, ip)
        db.session.commit()

        return "SUCCESS", {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    except Exception as e:
        app.logger.error(f"[CallbackGOOGLE] Internal error: {str(e)}")
        return "SERVER_ERROR", None