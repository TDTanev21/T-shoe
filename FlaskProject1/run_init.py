from flask import Flask
from config import Config
from models import db, login_manager

app = Flask(__name__)
app.config.from_object(Config)

# Важни настройки за Flask-Login
app.config['REMEMBER_COOKIE_DURATION'] = 3600  # 1 час
app.config['SESSION_PROTECTION'] = 'strong'

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Моля, влезте в системата за достъп до тази страница.'
login_manager.login_message_category = 'info'

# Import and register blueprints
from controllers.main_controller import main_bp
from controllers.auth_controller import auth_bp
from controllers.dashboard_controller import dashboard_bp

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

@app.context_processor
def inject_current_user():
    from flask_login import current_user
    return dict(current_user=current_user)

# Automatically create tables on startup
with app.app_context():
    db.create_all()
    print("✓ Database tables created/verified")

if __name__ == '__main__':
    app.run(debug=True)