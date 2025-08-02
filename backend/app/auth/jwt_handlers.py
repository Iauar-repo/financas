from app.core.responses import response


def register_jwt_callbacks(jwt, app):
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return response("TOKEN_EXPIRED")

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        return response("TOKEN_INVALID")

    @jwt.unauthorized_loader
    def missing_token_callback(reason):
        return response("TOKEN_MISSING")

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return response("TOKEN_REVOKED")
