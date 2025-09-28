from flask import render_template, redirect, url_for, flash, request
from . import auth_bp
from .forms import RegistrationForm
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
    except Exception as e:
        print(f"Registration Error: {e}")
        return redirect(url_for('errors.integrity_error'))
    return render_template('auth/register.html', form=form)



