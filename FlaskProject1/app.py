from flask import Flask,render_template
app = Flask(__name__)



from .main import main_bp

app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run()