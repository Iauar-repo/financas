from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from .extensions import db, jwt, cors, limiter
from .config import config_dict
from .logger import setup_logger

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
    
    # blueprints
    from app.auth import auth_bp
    from app.users import users_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    
    for rule in app.url_map.iter_rules():
        print(rule)
    
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
        # Trata erros HTTP padrão
        return jsonify({
            "error": e.name,
            "message": e.description,
            "status_code": e.code
        }), e.code
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        # Trata todos os outros erros inesperados
        app.logger.error(f"Erro inesperado: {str(e)}")
        return jsonify({
            "error": "Internal Server Error",
            "message": "Ocorreu um erro inesperado no servidor",
            "status_code": 500
        }), 500
    
    # Verificação de variáveis de ambiente carregadas
    app.config['ENV'] = 'production' if config_name == 'prod' else 'development'
    print(f"\n=== Configuração Carregada ===")
    print(f"Tipo: {config_name}")
    print(f"ENV: {app.config['ENV']}")
    print("============================\n")
    
    return app