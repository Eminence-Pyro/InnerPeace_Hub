from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import Admin, db
from utils import validate_password_strength

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        # Validate input
        if not username or not password:
            flash('Username and password are required', 'error')
            return render_template('admin/login.html')

        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password_hash(admin.password, password):
            login_user(admin, remember=True)
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('admin.admin_dashboard'))

        flash('Invalid username or password', 'error')

    return render_template('admin/login.html')


@auth_bp.route('/admin/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validate current password
        from flask_login import current_user
        if not check_password_hash(current_user.password, current_password):
            flash('Current password is incorrect', 'error')
            return render_template('admin/change_password.html')

        # Validate new password
        if new_password != confirm_password:
            flash('New passwords do not match', 'error')
            return render_template('admin/change_password.html')

        # Check password strength
        is_valid, message = validate_password_strength(new_password)
        if not is_valid:
            flash(message, 'error')
            return render_template('admin/change_password.html')

        # Update password
        from flask_login import current_user
        current_user.password = generate_password_hash(new_password)
        db.session.commit()

        flash('Password changed successfully', 'success')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin/change_password.html')


@auth_bp.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('auth.admin_login'))
