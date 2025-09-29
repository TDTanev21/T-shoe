from flask import render_template, redirect, url_for, flash, request, session
from flask_login import logout_user, login_manager, login_required

from . import auth_bp
from .forms import RegistrationForm, LoginForm
from .accounts import current_user

@auth_bp.route('/register', methods=['GET', 'POST'])
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    try:
        if request.method == 'POST':
            password = form.password.data
            confirm = form.confirm_password.data
            username = form.username.data
            if password != confirm:
                flash('Passwords do not match', 'danger')
                return render_template('auth/register.html', form=form)
            if username in [u[0] for u in current_user.accounts]:
                flash('Username already taken.', 'warning')
                return render_template('auth/register.html', form=form)
            current_user.accounts.append((username, password))
            print(current_user.accounts)
            return render_template('auth/login.html', form=form)

    except Exception as e:
        print(f"Registration Error: {e}")
        return redirect(url_for('errors.integrity_error'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            if (username, password) in current_user.accounts:
                session['username'] = username
                flash('Успешен вход!', 'success')
                current_user.is_authenticated = True
                return redirect(url_for('dashboard.dashboard'))

            flash('Невалидно потребителско име или парола.', 'danger')

        return render_template('auth/login.html', form=form)

    except Exception as e:
        print(f"Login Error: {e}")
        flash('Възникна критична грешка.', 'danger')
        return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    current_user.is_authenticated = False
    return redirect(url_for('main_bp.index'))