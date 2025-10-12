from flask import Blueprint, render_template
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required, logout_user
from models import User,db
import os
from werkzeug.utils import secure_filename
from flask import current_app

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/upload_picture', methods=['POST'])
def upload_picture():
    if 'profile_picture' not in request.files:
        flash('No file selected')
        return redirect(url_for('profile.settings'))

    file = request.files['profile_picture']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('profile.settings'))

    if file:
        filename = secure_filename(f"{current_user.username}_pfp.png")
        save_path = os.path.join(current_app.root_path, 'static', 'images', filename)

        file.save(save_path)
        flash('Profile picture updated successfully!')

    return redirect(url_for('profile.settings'))

@profile_bp.route('/settings', methods=['GET'])
@login_required
def settings():
    return render_template('profile/settings.html', current_user=current_user)

@profile_bp.route('/update_username', methods=['POST'])
@login_required
def update_username():
    try:
        new_username = request.form.get('username')
        if not new_username:
            flash('Username cannot be empty', 'danger')
            return redirect(url_for('profile.settings'))

        existing = User.query.filter_by(username=new_username).first()
        if existing and existing.id != current_user.id:
            flash('Username already taken', 'danger')
            return redirect(url_for('profile.settings'))

        current_user.username = new_username
        db.session.commit()
        flash('Username updated successfully', 'success')
    except Exception as e:
        print(f"Username Update Error: {e}")
        return redirect(url_for('errors.forbidden_error'))

    return redirect(url_for('profile.settings'))

@profile_bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    try:
        current_pw = request.form.get('current_password')
        new_pw = request.form.get('new_password')
        if not current_pw or not new_pw:
            flash('Both fields are required', 'danger')
            return redirect(url_for('profile.settings'))

        if not current_user.verify_password(current_pw):
            flash('Current password incorrect', 'danger')
            return redirect(url_for('profile.settings'))

        current_user.password = new_pw
        db.session.commit()
        flash('Password updated successfully', 'success')
    except Exception as e:
        print(f"Password Change Error: {e}")
        return redirect(url_for('errors.forbidden_error'))

    return redirect(url_for('profile.settings'))

@profile_bp.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    try:
        user = User.query.get(current_user.id)
        logout_user()
        if user:
            db.session.delete(user)
            db.session.commit()
            flash('Your account has been deleted.', 'success')
        else:
            flash('User not found.', 'error')
    except Exception as e:
        print(f"Account Deletion Error: {e}")
        return redirect(url_for('errors.forbidden_error'))

    return redirect(url_for('auth.login'))