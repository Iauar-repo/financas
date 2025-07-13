from flask import current_app as app
from marshmallow import ValidationError
from flask_bcrypt import generate_password_hash

from app.extensions import db
from app.models import Users
from app.users.schemas import user_schema, users_schema

# helper: insert novo usuário
def _insertUser(input):
    db.session.add(Users(
        name = input.get('name'),
        email = input.get('email'),
        username = input.get('username'),
        password = generate_password_hash(input.get('password')).decode('utf-8')
    ))

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

# main: new Users
def createUser_(input):
    try:
        data = user_schema.load(input)
        _insertUser(data)
        db.session.commit()
        
        return {"message": f"Usuário {data['username']} registrado"}, None, 200
    
    except ValidationError as e:
        db.session.rollback()
        app.logger.error(f"[NewUser] Input inválido: {str(e.messages)}")
        return None, e.messages, 400
    
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"[NewUser] Erro desconhecido ao registrar novo User: {str(e)}")
        return None, f"Erro desconhecido: {str(e)}", 500