from flask import Flask
from app.todo.routes import todo_bp
from app.auth.routes import auth_bp

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(todo_bp, url_prefix='/')
    
    return app