from flask import url_for
from flask_login import login_user as flask_login_user, logout_user
from models.user import User
from models import db

def register_user(username, password, confirm_password):
    """
    Регистрира нов потребител
    """
    try:
        # Проверка за съвпадение на паролите
        if password != confirm_password:
            return False, 'Паролите не съвпадат'

        # Проверка дали потребителското име е заето
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return False, 'Потребителското име е заето.'

        # Създаване на нов потребител
        user = User(username=username)
        user.set_password(password)

        # Записване в базата данни
        db.session.add(user)
        db.session.commit()

        return True, 'Регистрацията е успешна! Моля, влезте в системата.'

    except Exception as e:
        db.session.rollback()
        return False, f'Възникна грешка при регистрация: {str(e)}'

def login_user_service(username, password):
    """
    Вход на потребител
    """
    try:
        print(f"🔐 Attempting login for user: {username}")

        # Търсене на потребителя в базата данни
        user = User.query.filter_by(username=username).first()

        if user:
            print(f"✅ User found: {user.username}")

            # Проверка на паролата - използвай check_password
            password_correct = user.check_password(password)
            print(f"🔑 Password check: {password_correct}")

            if password_correct:
                # Логин на потребителя с Flask-Login
                flask_login_user(user)
                print(f"🚀 Login successful")
                print(f"👤 User authenticated: {user.is_authenticated}")

                # Определяне на пренасочването според ролята
                if user.is_admin:
                    redirect_url = url_for('dashboard.admin')
                    print("🎯 Redirecting to admin dashboard")
                else:
                    redirect_url = url_for('dashboard.dashboard')
                    print("🎯 Redirecting to user dashboard")

                return True, 'Успешен вход!', redirect_url
            else:
                print("❌ Incorrect password")
                return False, 'Невалидна парола.', url_for('auth.login')
        else:
            print("❌ User not found")
            return False, 'Потребителското име не съществува.', url_for('auth.login')

    except Exception as e:
        print(f"💥 Login error: {e}")
        return False, f'Възникна грешка при вход: {str(e)}', url_for('auth.login')

def logout_user_service():
    """
    Изход на потребител
    """
    logout_user()
    return True, 'Успешно излязохте от системата.'