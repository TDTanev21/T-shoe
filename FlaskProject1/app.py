from flask import Flask
from config import Config
app = Flask(__name__)
app.config['SECRET_KEY'] = 'VERYSECRETKEY'


from main import main_bp
from auth import auth_bp
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
if __name__ == '__main__':
    app.run()