from flask import Flask
from config import Config
from models import db, login_manager

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Моля, влезте в системата за достъп до тази страница.'
login_manager.login_message_category = 'info'

from controllers.main_controller import main_bp
from controllers.auth_controller import auth_bp
from controllers.dashboard_controller import dashboard_bp
from controllers.cart_controller import cart_bp
from controllers.profile_controller import profile_bp
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(cart_bp, url_prefix='/cart')

app.register_blueprint(profile_bp, url_prefix='/profile')
@app.context_processor
def inject_current_user():
    from flask_login import current_user
    return dict(current_user=current_user)

with app.app_context():
    db.create_all()
    print(" Database tables created/verified")

if __name__ == '__main__':
    app.run(debug=True)
