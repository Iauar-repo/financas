from flask import current_app as app
from marshmallow import ValidationError
from flask_bcrypt import generate_password_hash

from app.extensions import db
from app.models import Users
from app.users.schemas import user_schema, users_schema, updateUser_schema
from app.auth.utils import send_confirmation_email

# helper: insert novo usuário
def _insertUser(input):
    db.session.add(Users(
        name = input.get('name'),
        email = input.get('email'),
        username = input.get('username'),
        password = generate_password_hash(input.get('password')).decode('utf-8')
    ))

# helper: atualiza usuário
def _updateUser(data, user):
    blacklist = ['ID', 'is_admin', 'email_confirmed']

    for key,val in data.items():
        if key not in blacklist:
            if key == 'password':
                val = generate_password_hash(val).decode('utf-8')
            setattr(user, key, val)

# main: dump Users
def listUsers_(id: int = 0):
    try:
        if id != 0:
            user = Users.query.get(id)
            if not user:
                app.logger.error(f"[DumpUser] Usuário não existe. ID: {id}")
                return None, "Usuário não existe", 404
            
            return user_schema.dump(user), None, 200
        
        users = Users.query.all()
        return users_schema.dump(users), None, 200
    
    except Exception as e:
        app.logger.error(f"[DumpUser] Erro desconhecido ao buscar infos do usuário: {str(e)}")
        return None, f"Erro desconhecido: {str(e)}", 500

# main: new User
def createUser_(input):
    try:
        data = user_schema.load(input)
        _insertUser(data)
        db.session.commit()

        user = Users.query.filter_by(email=data['email']).first()
        send_confirmation_email(user)
        
        return {"message": f"Usuário {data['username']} registrado"}, None, 200
    
    except ValidationError as e:
        db.session.rollback()
        app.logger.error(f"[NewUser] Input inválido: {str(e.messages)}")
        return None, e.messages, 400
    
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"[NewUser] Erro desconhecido ao registrar novo User: {str(e)}")
        return None, f"Erro desconhecido: {str(e)}", 500

# main: update User
def updateUser_(input, user_id):
    try:
        user = Users.query.get(user_id)
        if not user:
                app.logger.error(f"[UpdateUser] Usuário não existe. ID: {user_id}")
                return None, "Usuário não existe", 404
        
        data = updateUser_schema.load(input, partial=True)
        _updateUser(data, user)
        db.session.commit()
        
        return user_schema.dump(user), None, 200
    
    except ValidationError as e:
        db.session.rollback()
        app.logger.error(f"[UpdateUser] Input inválido: {str(e.messages)}")
        return None, e.messages, 400
    
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"[UpdateUser] Erro desconhecido ao atualizar User: {str(e)}")
        return None, f"Erro desconhecido: {str(e)}", 500

# main: delete User
def deleteUser_(user_id):
    try:
        user = Users.query.get(user_id)
        name = user.name
        if not user:
                app.logger.error(f"[DeleteUser] Usuário não existe. ID: {user_id}")
                return None, "Usuário não existe", 404
        
        db.session.delete(user)
        db.session.commit()

        return {"message": f"Usuário {name} foi deletado"}, None, 200
    
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"[DeleteUser] Erro desconhecido ao deletar User: {str(e)}")
        return None, f"Erro desconhecido: {str(e)}", 500
