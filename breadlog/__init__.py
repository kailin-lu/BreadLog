from flask import Flask
from breadlog.config import Config
from .extensions import db, login_manager, bcrypt   

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    
    db.init_app(app) 
    login_manager.init_app(app)
    login_manager.login_view = '__users.login__'
    bcrypt.init_app(app) 
    
    from breadlog.users.routes import users 
    from breadlog.recipes.routes import recipes 
    from breadlog.about.routes import about 
    from breadlog.errors.handlers import errors

    app.register_blueprint(users) 
    app.register_blueprint(recipes) 
    app.register_blueprint(about)
    app.register_blueprint(errors) 
    
    return app 
    
