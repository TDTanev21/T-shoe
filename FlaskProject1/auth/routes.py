from flask import render_template, redirect, url_for, flash, session, request
from flask_login import login_user, logout_user, current_user
from . import auth_bp
from .forms import LoginForm, RegistrationForm
from data.accounts import *

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
            if username in accounts:
                flash('Username already taken.', 'warning')
                return render_template('auth/register.html', form=form)
            accounts.append((username, password))
    except Exception as e:
        print(f"Registration Error: {e}")
        return redirect(url_for('errors.integrity_error'))
    return render_template('auth/register.html', form=form)


