from flask_jwt_extended import create_access_token, create_refresh_token, get_jti

# gera novos tokens
def generate_tokens(user_id):
    access = create_access_token(identity=str(user_id))
    refresh = create_refresh_token(identity=str(user_id))
    jti_acc = get_jti(access)
    jti_ref = get_jti(refresh)

    return access, refresh, jti_acc, jti_ref
