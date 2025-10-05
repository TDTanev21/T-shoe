from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from models.user import current_user, accounts
from services.auth_service import register_user, login_user, logout_user
from models.forms import LoginForm,RegistrationForm
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()

    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        success, message = register_user(username, password, confirm_password)
        flash(message, 'success' if success else 'danger')

        if success:
            return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        success, message, redirect_url = login_user(username, password, session)
        flash(message, 'success' if success else 'danger')

        if success:
            return redirect(redirect_url)

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user(session)
    flash('Успешно излязохте от системата.', 'info')
    return redirect(url_for('main_bp.index'))