from flask import Flask
from config import Config
from auth.accounts import current_user
app = Flask(__name__)
app.config['SECRET_KEY'] = 'VERYSECRETKEY'


from main import main_bp
from auth import auth_bp
from dashboard import dashboard_bp
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
if __name__ == '__main__':
    app.run()

@app.context_processor
def inject_current_user():
    return dict(current_user=current_user)