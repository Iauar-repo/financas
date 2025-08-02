from app.auth.utils import send_confirmation_email
from app.extensions import db
from flask import current_app as app
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from .repository import (
    get_all_users,
    get_user_by_email,
    get_user_by_id,
    insert_provider,
    insert_user,
    update_user,
)
from .schemas import (
    create_user_schema,
    list_user_schema,
    list_users_schema,
    update_user_schema,
)
from .utils import verify_recaptcha


def list_users_(user_id: int = 0):
    try:
        if user_id != 0:
            user = get_user_by_id(user_id)
            if not user:
                app.logger.error(f"[DumpUser] User not found: {user_id}")
                return "USER_NOT_FOUND", None

            return "SUCCESS", list_user_schema.dump(user)

        users = get_all_users()
        return "SUCCESS", list_users_schema.dump(users)

    except Exception as e:
        app.logger.error(f"[DumpUser] Internal error: {str(e)}")
        return "SERVER_ERROR", None


def create_user_(input: dict):
    try:
        data = create_user_schema.load(input)
        recaptcha_token = data["recaptcha_token"]
        if not recaptcha_token or not verify_recaptcha(recaptcha_token):
            return "RECAPTCHA_INVALID", None

        insert_user(data)
        db.session.flush()
        user = get_user_by_email(data["email"])
        insert_provider(user.id, "email", data["email"], data["password"])
        db.session.commit()
        send_confirmation_email(user)

        return "CREATED", list_user_schema.dump(user)

    except ValidationError as e:
        app.logger.error(f"[CreateUser] Invalid payload: {str(e.messages)}")
        return "INVALID_PAYLOAD", {"error": str(e.messages)}

    except IntegrityError as e:
        db.session.rollback()
        app.logger.error(f"[CreateUser] Duplicate: {str(e)}")
        return "USER_ALREADY_EXISTS", {"error": str(e.orig)}

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"[CreateUser] Internal error: {str(e)}")
        return "SERVER_ERROR", None


def update_user_(input: dict, user_id: int):
    try:
        user = get_user_by_id(user_id)
        if not user:
            app.logger.error(f"[UpdateUser] User not found: {user_id}")
            return "USER_NOT_FOUND", None

        data = update_user_schema.load(input, partial=True)
        update_user(data, user)
        db.session.commit()

        return "SUCCESS", list_user_schema.dump(user)

    except ValidationError as e:
        db.session.rollback()
        app.logger.error(f"[UpdateUser] Invalid payload: {str(e.messages)}")
        return "INVALID_PAYLOAD", {"error": str(e.messages)}

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"[UpdateUser] Internal error: {str(e)}")
        return "SERVER_ERROR", None


def delete_user_(user_id: int):
    try:
        user = get_user_by_id(user_id)
        if not user:
            app.logger.error(f"[DeleteUser] User not found: {user_id}")
            return "USER_NOT_FOUND", None

        db.session.delete(user)
        db.session.commit()
        return "SUCCESS", None

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"[DeleteUser] Internal error: {str(e)}")
        return "SERVER_ERROR", None
