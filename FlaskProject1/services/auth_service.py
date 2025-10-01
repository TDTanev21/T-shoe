from flask import url_for

from models.user import accounts, current_user


def register_user(username, password, confirm_password):
    if password != confirm_password:
        return False, 'Паролите не съвпадат'

    if username in [u[0] for u in accounts]:
        return False, 'Потребителското име е заето.'

    accounts.append((username, password))
    print(f"Нов потребител: {username}")
    print(f"Всички потребители: {accounts}")

    return True, 'Регистрацията е успешна! Моля, влезте в системата.'


def login_user(username, password, session):
    if (username, password) in accounts:
        session['username'] = username
        current_user.username = username
        current_user.is_authenticated = True

        redirect_url = url_for('dashboard.admin') if username == "admin" else url_for('dashboard.dashboard')
        return True, 'Успешен вход!', redirect_url
    else:
        return False, 'Невалидно потребителско име или парола.', url_for('auth.login')


def logout_user(session):
    session.pop('username', None)
    current_user.username = None
    current_user.is_authenticated = False