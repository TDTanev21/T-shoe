from flask import Flask
from config import Config
from models import db, login_manager

app = Flask(__name__)
app.config.from_object(Config)

# ДОБАВИ ТЕЗИ РЕДОВЕ:
app.config['DEBUG'] = True
app.config['TESTING'] = True

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
from controllers.review_controller import review_bp
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(cart_bp, url_prefix='/cart')
app.register_blueprint(profile_bp, url_prefix='/profile')
app.register_blueprint(review_bp, url_prefix='/review')
@app.context_processor
def inject_current_user():
    from flask_login import current_user
    return dict(current_user=current_user)
with app.app_context():
    try:
        from models.user import User
        from models.product import Shoe, SportShoe, FormalShoe, CasualShoe
        from models.order import Order, OrderItem
        from models.review import Review

        db.create_all()
        print("✅ Database tables created/verified")
    except Exception as e:
        print(f"❌ Database error: {e}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)