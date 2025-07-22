from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from .extensions import db, jwt, cors, limiter, mail, oauth
from .config import config_dict
from .logger import setup_logger
from .core.responses import response

def create_app(config_name='default'):
    app = Flask(__name__)
    
    if config_name not in config_dict:
        raise ValueError(f"Config '{config_name}' not found")
    
    app.config.from_object(config_dict[config_name])
    
    setup_logger(app)
    db.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    mail.init_app(app)
    oauth.init_app(app)

    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        access_token_url='https://oauth2.googleapis.com/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        api_base_url='https://www.googleapis.com/oauth2/v2/',
        client_kwargs={'scope': 'email profile'},
    )
    
    # blueprints
    from app.auth import auth_bp
    from app.users import users_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    
    #for rule in app.url_map.iter_rules():
    #    print(rule)
    
    # callback JWT
    from app.models import TokenBlocklist
    from app.auth import jwt_handlers

    jwt_handlers.register_jwt_callbacks(jwt, app)
    
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token = TokenBlocklist.query.filter_by(jti=jti).first()
        return token is not None
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify({
            "error": e.name,
            "message": e.description,
            "status_code": e.code
        }), e.code
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        app.logger.error(f"Unexpected error: {str(e)}")
        return response("UNEXPECTED_ERROR", None)
    
    # Verificação de variáveis de ambiente carregadas
    app.config['ENV'] = 'production' if config_name == 'prod' else 'development'
    print(f"\n=== Config loaded ===")
    print(f"Tipo: {config_name}")
    print(f"ENV: {app.config['ENV']}")
    print("============================\n")
    
    return app
