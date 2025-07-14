from app.extensions import db
from datetime import datetime, timezone, timedelta

class Users(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(320), nullable=False, unique=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Integer, default=lambda: 0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    active = db.relationship("ActiveSessions", backref="user", cascade="all, delete", passive_deletes=True)
    blocklist = db.relationship("TokenBlocklist", backref="user", cascade="all, delete", passive_deletes=True)

    def __repr__(self):
        return f'<Name {self.name}>'

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
