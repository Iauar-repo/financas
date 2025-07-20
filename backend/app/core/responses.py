from flask import jsonify

MESSAGES = {
    'SUCCESS': ('Operation successful.', 200),
    'CREATED': ('Resource created successfully.', 201),
    'INVALID_PAYLOAD': ('Invalid request payload.', 400),
    'USER_ALREADY_EXISTS': ('User already exists.', 400),
    'USER_NOT_FOUND': ('User not found.', 404),
    'UNAUTHENTICATED': ('Unauthenticated.', 401),
    'FORBIDDEN': ('Access denied.', 403),
    'LOGIN_FAILED': ('Login failed.', 401),
    'TOKEN_INVALID': ('Invalid token.', 422),
    'TOKEN_EXPIRED': ('Token expired.', 401),
    'TOKEN_REVOKED': ('Token revoked.', 401),
    'TOKEN_MISSING': ('Missing token.', 401),
    'RECAPTCHA_INVALID': ('Invalid reCAPTCHA.', 400),
    'OAUTH_ERROR': ('OAuth authentication failed.', 400),
    'SERVER_ERROR': ('Internal server error.', 500),
    'UNKNOWN_ERROR': ('An unknown error occurred.', 500),
}

def response(key: str, data: dict = None):
    message, code = MESSAGES.get(key, MESSAGES['UNKNOWN_ERROR'])
    payload = {'message': message}
    if data:
        payload['data'] = data

    return jsonify(payload), code
