from app.extensions import db
from app.models import Users, AuthProvider
from flask_bcrypt import generate_password_hash

def insert_user(data):
    db.session.add(Users(
        name = data.get('name'),
        email = data.get('email')
    ))

def update_user(data, user):
    blacklist = ['ID', 'is_admin', 'email_confirmed']
    for key,val in data.items():
        if key not in blacklist:
            if key == 'password':
                val = generate_password_hash(val).decode('utf-8')
            setattr(user, key, val)

def insert_provider(user_id, provider, provider_id, password):
    db.session.add(AuthProvider(
        user_id = user_id,
        provider = provider,
        provider_user_id = provider_id,
        password_hash = generate_password_hash(password).decode('utf-8')
    ))
