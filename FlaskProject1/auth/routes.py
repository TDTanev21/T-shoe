from flask import render_template, redirect, url_for, flash, request, session
from . import auth_bp
from .forms import RegistrationForm, LoginForm
from .accounts import current_user, accounts  # Импортирай и accounts


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            password = form.password.data
            confirm = form.confirm_password.data
            username = form.username.data

            if password != confirm:
                flash('Паролите не съвпадат', 'danger')
                return render_template('auth/register.html', form=form)

            if username in [u[0] for u in accounts]:
                flash('Потребителското име е заето.', 'warning')
                return render_template('auth/register.html', form=form)

            accounts.append((username, password))
            print(f"Нов потребител: {username}")
            print(f"Всички потребители: {accounts}")

            flash('Регистрацията е успешна! Моля, влезте в системата.', 'success')
            print("Регистрацията е успешна! Моля, влезте в системата.")
            return redirect(url_for('auth.login'))

    except Exception as e:
        print(f"Registration Error: {e}")
        flash('Възникна грешка при регистрацията.', 'danger')
        return redirect(url_for('auth.register'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            if (username, password) in accounts:
                session['username'] = username
                current_user.username = username
                current_user.is_authenticated = True

                flash('Успешен вход!', 'success')

                if username == "admin":
                    return redirect(url_for('dashboard.admin'))
                return redirect(url_for('dashboard.dashboard'))
            else:
                flash('Невалидно потребителско име или парола.', 'danger')

    except Exception as e:
        print(f"Login Error: {e}")
        flash('Възникна критична грешка.', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    current_user.username = None
    current_user.is_authenticated = False
    flash('Успешно излязохте от системата.', 'info')
    return redirect(url_for('main_bp.index'))