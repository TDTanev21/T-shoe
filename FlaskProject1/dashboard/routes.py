from flask import render_template, session, redirect, url_for, flash
from auth.accounts import current_user
from . import dashboard_bp

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Моля, влезте в системата, за да видите дашборда.', 'warning')
        return redirect(url_for('auth.login'))

    current_user.username = session['username']
    return render_template('dashboard/dashboard.html', current_user=current_user)
@dashboard_bp.route('/dashboard/cart')
def cart():
    return render_template("dashboard/cart.html", current_user=current_user)
@dashboard_bp.route('/add')
def add():
    pass