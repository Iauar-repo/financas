from app.extensions import db
from app.models import ActiveSessions, AuthProvider, TokenBlocklist


def create_session(user_id: int, refresh_jti: str, ip: str):
    db.session.add(ActiveSessions(jti=refresh_jti, user_id=user_id, ip_address=ip))


def revoke_session(user_id: int, session: ActiveSessions):
    db.session.add(
        TokenBlocklist(
            jti=session.jti,
            user_id=user_id,
            ip_address=session.ip_address,
            created_at=session.created_at,
            expires_at=session.expires_at,
        )
    )
    db.session.delete(session)


def get_user_by_provider(provider: str, provider_user_id: str):
    ap = AuthProvider.query.filter_by(
        provider=provider, provider_user_id=provider_user_id
    ).first()

    return (None, None) if not ap else (ap.user, ap)


def get_session_by_jti(refresh_jti: str, user_id: int):
    session = ActiveSessions.query.filter_by(jti=refresh_jti, user_id=user_id).first()

    return session


def get_active_session(user_id: int):
    session = ActiveSessions.query.filter_by(user_id=user_id).first()

    return session
