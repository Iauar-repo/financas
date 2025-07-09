from app.extensions import db
from datetime import datetime, timezone, timedelta

class Users(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    nickname = db.Column(db.String(10), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Name {self.name}>'

class ActiveSessions(db.Model):
    __tablename__ = 'activesessions'
    
    jti = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    expires_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=7))

    def __repr__(self):
        return f"<Token {self.jti}>"

class TokenBlocklist(db.Model):
    __tablename__ = 'tokenblocklist'
    
    jti = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    revoked_at = db.Column(db.DateTime, default=datetime.now(timezone.utc).replace(tzinfo=None))

    def __repr__(self):
        return f"<Token {self.jti}>"
