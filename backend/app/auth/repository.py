from app.extensions import db
from app.models import ActiveSessions, TokenBlocklist, AuthProvider

def create_session(user_id: int, refresh_jti: str, ip: str):
    """
    Create a new active session for a user.

    Parameters:
        id (int): ID of the user initiating the session.
        refresh_jti (str): Unique identifier (JTI) of the refresh token.
        ip (str): IP address from which the session is created.

    Returns:
        None
    """
    db.session.add(ActiveSessions(
        jti = refresh_jti,
        user_id = user_id,
        ip_address = ip
    ))

def revoke_session(user_id: int, session: ActiveSessions):
    """
    Revoke an active session by transferring its data to the token blocklist.

    Parameters:
        id (int): ID of the user whose session is being revoked.
        session (ActiveSessions): Active session object to be revoked.

    Returns:
        None
    """    
    db.session.add(TokenBlocklist(
        jti = session.jti,
        user_id = user_id,
        ip_address = session.ip_address,
        created_at = session.created_at,
        expires_at = session.expires_at
    ))
    db.session.delete(session)

def get_user_by_provider(provider: str, provider_user_id: str):
    """
    Retrieve a user instance by provider method and ID

    Parameters:
        provider (str): Provider type (e.g., email, google).
        provider_user_id (str): Provider ID.
    
    Returns:
        Users: SQLAlchemy User instance
    """        
    ap = AuthProvider.query.filter_by(
        provider=provider,
        provider_user_id=provider_user_id
        ).first()
    
    return (None, None) if not ap else (ap.user, ap)

def get_session_by_jti(refresh_jti: str, user_id: int):
    session = ActiveSessions.query.filter_by(
        jti=refresh_jti,
        user_id=user_id
        ).first()
    
    return session

def get_active_session(user_id: int):
    session = ActiveSessions.query.filter_by(
        user_id=user_id
        ).first()
    
    return session

