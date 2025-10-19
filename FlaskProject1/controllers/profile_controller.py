from flask import Blueprint, render_template
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required, logout_user
from models.user import User  # Промени този импорт
from models import db
import os
from werkzeug.utils import secure_filename
from flask import current_app

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/settings')
@login_required
def settings():
    username = current_user.username
    approved_path = os.path.join(current_app.root_path, 'static', 'images', f"{username}_pfp.png")
    pending_path = os.path.join(current_app.root_path, 'static', 'pending_pictures', f"{username}_pending.png")

    approved_exists = os.path.exists(approved_path)
    pending_exists = os.path.exists(pending_path)

    return render_template(
        'profile/settings.html',
        current_user=current_user,
        approved_exists=approved_exists,
        pending_exists=pending_exists
    )

@profile_bp.route('/upload_picture', methods=['POST'])
@login_required
def upload_picture():
    if 'profile_picture' not in request.files or request.files['profile_picture'].filename == '':
        flash('Не е избран файл.')
        return redirect(url_for('profile.settings'))

    file = request.files['profile_picture']
    filename = secure_filename(f"{current_user.username}_pending.png")

    pending_folder = os.path.join(current_app.root_path, 'static', 'pending_pictures')
    os.makedirs(pending_folder, exist_ok=True)

    save_path = os.path.join(pending_folder, filename)
    file.save(save_path)

    flash('Снимката е качена и чака одобрение от администратор.')
    return redirect(url_for('profile.settings'))

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
        flash('Грешка при обновяване на потребителското име', 'danger')
        return redirect(url_for('profile.settings'))

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

        # Използвай check_password, както е в User модела
        if not current_user.check_password(current_pw):
            flash('Current password incorrect', 'danger')
            return redirect(url_for('profile.settings'))

        current_user.set_password(new_pw)
        db.session.commit()
        flash('Password updated successfully', 'success')
    except Exception as e:
        print(f"Password Change Error: {e}")
        flash('Грешка при промяна на паролата', 'danger')
        return redirect(url_for('profile.settings'))

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
        flash('Грешка при изтриване на акаунта', 'danger')
        return redirect(url_for('profile.settings'))

    return redirect(url_for('auth.login'))