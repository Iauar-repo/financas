from flask import current_app as app
from marshmallow import ValidationError

from app.extensions import db
from app.models import Users
from app.auth.utils import send_confirmation_email
from app.auth.repository import get_user_by_email

from .schemas import listUser_schema, listUsers_schema, updateUser_schema, createUser_schema
from .utils import verify_recaptcha
from .repository import insert_user, update_user, insert_provider

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
        data = createUser_schema.load(input)
        recaptcha_token = data['recaptcha_token']
        if not recaptcha_token or not verify_recaptcha(recaptcha_token):
            return "RECAPTCHA_INVALID", None

        insert_user(data)
        db.session.flush()        
        user = get_user_by_email(data['email'])
        if not user:
            raise Exception('Could not create user')
        
        insert_provider(user.id, 'email', data['email'], data['password'])
        db.session.commit()
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
