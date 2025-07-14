from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jti,
    verify_jwt_in_request,
    get_jwt,
    get_jwt_identity
)
from functools import wraps
from flask import jsonify

# gera novos tokens
def generate_tokens(user_id, is_admin):
    access = create_access_token(
        identity=str(user_id),
        additional_claims={"is_admin": is_admin}
    )
    refresh = create_refresh_token(
        identity=str(user_id),
        additional_claims={"is_admin": is_admin}
    )
    jti_acc = get_jti(access)
    jti_ref = get_jti(refresh)

    return access, refresh, jti_acc, jti_ref

# decorador admin_required
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if not claims.get("is_admin"):
            return jsonify(message="Acesso negado"), 403
        return fn(*args, **kwargs)
    return wrapper

# decorador owner_or_admin_required
def owner_or_admin_required(fn):
    @wraps(fn)
    def wrapper(user_id, *args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        current_user_id = int(get_jwt_identity())

        if not claims.get("is_admin") and current_user_id != user_id:
            return jsonify(message="Acesso negado"), 403

        return fn(user_id, *args, **kwargs)
    return wrapper
