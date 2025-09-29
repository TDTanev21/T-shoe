import os

from flask import Flask
from flask_login import LoginManager
from auth.accounts import current_user

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "some_very_secret_key")

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    for user in current_user.accounts:
        if user.username == user_id:
            return user
    return None

from main import main_bp
from auth import auth_bp
from dashboard import dashboard_bp

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')

app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

@app.context_processor
def inject_current_user():
    return dict(current_user=current_user)

if __name__ == '__main__':
    app.run(debug=True)
