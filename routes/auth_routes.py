from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from models import Admin, db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password_hash(admin.password, password):
            login_user(admin)
            return redirect(url_for('admin.admin_dashboard'))

        flash('Invalid username or password')

    return render_template('admin/login.html')


@auth_bp.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('auth.admin_login'))
