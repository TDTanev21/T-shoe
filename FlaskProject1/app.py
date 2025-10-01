import os
from flask import Flask
from flask_login import LoginManager
from models.user import current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'VERYSECRETKEY'

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    for username, password in current_user.accounts:
        if username == user_id:
            return current_user
    return None

from controllers.main_controller import main_bp
from controllers.auth_controller import auth_bp
from controllers.dashboard_controller import dashboard_bp

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

@app.context_processor
def inject_current_user():
    return dict(current_user=current_user)

if __name__ == '__main__':
    app.run(debug=True)