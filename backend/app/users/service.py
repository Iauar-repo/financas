from flask import current_app as app
from marshmallow import ValidationError
from flask_bcrypt import generate_password_hash
import requests
from app.extensions import db
from app.models import Users
from app.users.schemas import listUser_schema, listUsers_schema, updateUser_schema, createUser_schema
from app.auth.utils import send_confirmation_email

# helper: insert new user
def _insertUser(input):
    db.session.add(Users(
        name = input.get('name'),
        email = input.get('email'),
        username = input.get('username'),
        password = generate_password_hash(input.get('password')).decode('utf-8')
    ))

# helper: update user
def _updateUser(data, user):
    blacklist = ['ID', 'is_admin', 'email_confirmed']
    for key,val in data.items():
        if key not in blacklist:
            if key == 'password':
                val = generate_password_hash(val).decode('utf-8')
            setattr(user, key, val)

# helper: verify recaptcha token
def verify_recaptcha(token):
    secret_key = app.config['RECAPTCHA_SECRET_KEY']
    url = 'https://www.google.com/recaptcha/api/siteverify'
    payload = {'secret': secret_key, 'response': token}
    response = requests.post(url, data=payload)
    result = response.json()
    return result.get('success', False)

# main: dump Users
def listUsers_(id: int = 0):
    try:
        if id != 0:
            user = Users.query.get(id)
            if not user:
                app.logger.error(f"[DumpUser] User not found. ID: {id}")
                return "USER_NOT_FOUND", None
            
            return "SUCCESS", listUser_schema.dump(user)
        
        users = Users.query.all()
        return "SUCCESS", listUsers_schema.dump(users)
    
    except Exception as e:
        app.logger.error(f"[DumpUser] Internal error: {str(e)}")
        return "SERVER_ERROR", {"error":str(e)}

# main: new User
def createUser_(input):
    try:
        recaptcha_token = input.get('recaptcha_token')
        if not recaptcha_token or not verify_recaptcha(recaptcha_token):
            return "RECAPTCHA_INVALID", None

        data = createUser_schema.load(input)
        _insertUser(data)
        db.session.commit()

        user = Users.query.filter_by(email=data['email']).first()
        send_confirmation_email(user)
        
        return "CREATED", listUser_schema.dump(user)
    
    except ValidationError as e:
        db.session.rollback()
        app.logger.error(f"[NewUser] Invalid payload: {str(e.messages)}")
        return "INVALID_PAYLOAD", {"error":str(e.messages)}
    
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"[NewUser] Internal error: {str(e)}")
        return "SERVER_ERROR", {"error":str(e)}

# main: update User
def updateUser_(input, user_id):
    try:
        user = Users.query.get(user_id)
        if not user:
                app.logger.error(f"[UpdateUser] User not found. ID: {user_id}")
                return "USER_NOT_FOUND", None
        
        data = updateUser_schema.load(input, partial=True)
        _updateUser(data, user)
        db.session.commit()
        
        return "SUCCESS", listUser_schema.dump(user)
    
    except ValidationError as e:
        db.session.rollback()
        app.logger.error(f"[UpdateUser] Invalid payload: {str(e.messages)}")
        return "INVALID_PAYLOAD", {"error":str(e.messages)}
    
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"[UpdateUser] Internal error: {str(e)}")
        return "SERVER_ERROR", {"error":str(e)}

# main: delete User
def deleteUser_(user_id):
    try:
        user = Users.query.get(user_id)
        name = user.name
        if not user:
            app.logger.error(f"[DeleteUser] User not found. ID: {user_id}")
            return "USER_NOT_FOUND", None
        
        db.session.delete(user)
        db.session.commit()

        return "SUCCESS", None
    
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"[DeleteUser] Internal error: {str(e)}")
        return "SERVER_ERROR", {"error":str(e)}
