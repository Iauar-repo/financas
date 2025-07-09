from flask import jsonify

def register_jwt_callbacks(jwt, app):
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "error": "token_expired",
            "message": "O token fornecido expirou"
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        return jsonify({
            "error": "invalid_token",
            "message": "O token fornecido é inválido"
        }), 422

    @jwt.unauthorized_loader
    def missing_token_callback(reason):
        return jsonify({
            "error": "authorization_required",
            "message": "Token não fornecido"
        }), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "error": "token_revoked",
            "message": "O token fornecido está revogado"
        }), 401
