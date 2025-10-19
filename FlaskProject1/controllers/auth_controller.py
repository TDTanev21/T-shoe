from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.forms import LoginForm, RegistrationForm
from services.auth_service import register_user, login_user_service, logout_user_service

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Ако потребителят вече е логнат, пренасочваме
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('dashboard.admin'))
        else:
            return redirect(url_for('dashboard.dashboard'))

    form = RegistrationForm()

    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        # Регистриране на потребителя
        success, message = register_user(username, password, confirm_password)
        flash(message, 'success' if success else 'danger')

        if success:
            return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Ако потребителят вече е логнат, пренасочваме
    if current_user.is_authenticated:
        flash('Вече сте влезли в системата!', 'info')
        if current_user.is_admin:
            return redirect(url_for('dashboard.admin'))
        else:
            return redirect(url_for('dashboard.dashboard'))

    form = LoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        print(f"Login attempt - Username: {username}")

        # Вход на потребителя
        success, message, redirect_url = login_user_service(username, password)

        print(f"Login result - Success: {success}, Message: {message}")

        flash(message, 'success' if success else 'danger')

        if success:
            return redirect(redirect_url)

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    # Изход на потребителя
    success, message = logout_user_service()
    flash(message, 'info')
    return redirect(url_for('main.index'))