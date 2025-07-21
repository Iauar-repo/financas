from app.extensions import db
from datetime import datetime, timezone, timedelta

class Users(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(320), nullable=False, unique=True)
    is_admin = db.Column(db.Integer, nullable=False, default=0)
    email_confirmed = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    active = db.relationship("ActiveSessions", backref="user", cascade="all, delete", passive_deletes=True)
    blocklist = db.relationship("TokenBlocklist", backref="user", cascade="all, delete", passive_deletes=True)
    auth_providers = db.relationship('AuthProvider', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Name {self.name}>'


class AuthProvider(db.Model):
    __tablename__ = 'authproviders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id', ondelete='CASCADE'),nullable=False)
    provider = db.Column(db.String(20), nullable=False)
    provider_user_id = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(60))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    user = db.relationship('Users', back_populates='auth_providers')


class ActiveSessions(db.Model):
    __tablename__ = 'activesessions'
    
    jti = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    ip_address = db.Column(db.String(15), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    expires_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=7))

    def __repr__(self):
        return f"<Token {self.jti}>"

class TokenBlocklist(db.Model):
    __tablename__ = 'tokenblocklist'
    
    jti = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    ip_address = db.Column(db.String(15), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    revoked_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    def __repr__(self):
        return f"<Token {self.jti}>"
