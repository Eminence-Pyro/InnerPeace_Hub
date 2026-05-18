from flask import Blueprint, render_template, redirect, url_for, request, flash, session
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

        if not username or not password:
            flash('Username and password are required', 'error')
            return render_template('admin/login.html')

        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password_hash(admin.password, password):
            # ── Improvement 14: 2FA TOTP check ─────────────────────────────
            if admin.totp_enabled and admin.totp_secret:
                # Store admin id in session for the 2FA step, do NOT log in yet
                session['pending_2fa_user_id'] = admin.id
                return redirect(url_for('auth.verify_2fa'))

            login_user(admin, remember=True)
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('admin.admin_dashboard'))

        flash('Invalid username or password', 'error')

    return render_template('admin/login.html')


# ── Improvement 14: TOTP verification step ────────────────────────────────────
@auth_bp.route('/admin/2fa', methods=['GET', 'POST'])
def verify_2fa():
    user_id = session.get('pending_2fa_user_id')
    if not user_id:
        return redirect(url_for('auth.admin_login'))

    admin = Admin.query.get(user_id)
    if not admin:
        session.pop('pending_2fa_user_id', None)
        return redirect(url_for('auth.admin_login'))

    if request.method == 'POST':
        code = request.form.get('code', '').strip().replace(' ', '')
        try:
            import pyotp
            totp = pyotp.TOTP(admin.totp_secret)
            if totp.verify(code, valid_window=1):
                session.pop('pending_2fa_user_id', None)
                login_user(admin, remember=True)
                return redirect(url_for('admin.admin_dashboard'))
            else:
                flash('Invalid or expired code. Try again.', 'error')
        except ImportError:
            flash('2FA library not installed. Run: pip install pyotp', 'error')

    return render_template('admin/verify_2fa.html')


# ── Improvement 14: 2FA setup / toggle ───────────────────────────────────────
@auth_bp.route('/admin/2fa/setup', methods=['GET', 'POST'])
@login_required
def setup_2fa():
    admin = current_user
    try:
        import pyotp, qrcode, io, base64 as b64
        if request.method == 'POST':
            action = request.form.get('action')

            if action == 'enable':
                code = request.form.get('code', '').strip().replace(' ', '')
                secret = request.form.get('secret', '').strip()
                totp = pyotp.TOTP(secret)
                if totp.verify(code, valid_window=1):
                    admin.totp_secret  = secret
                    admin.totp_enabled = True
                    db.session.commit()
                    flash('Two-factor authentication enabled! ✅', 'success')
                    return redirect(url_for('admin.admin_dashboard'))
                else:
                    flash('Code did not match. Please try again.', 'error')
                    secret = secret  # keep the same secret

            elif action == 'disable':
                admin.totp_enabled = False
                db.session.commit()
                flash('Two-factor authentication disabled.', 'success')
                return redirect(url_for('admin.admin_dashboard'))

        # Generate new secret for display
        secret = admin.totp_secret or pyotp.random_base32()
        totp   = pyotp.TOTP(secret)
        uri    = totp.provisioning_uri(name=admin.username, issuer_name='InnerPeace Hub')

        # Generate QR code
        img = qrcode.make(uri)
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        qr_b64 = b64.b64encode(buf.getvalue()).decode()

        return render_template('admin/setup_2fa.html',
                               admin=admin, secret=secret, qr_b64=qr_b64)

    except ImportError as e:
        flash(f'2FA requires: pip install pyotp qrcode[pil]  — {e}', 'error')
        return redirect(url_for('admin.admin_dashboard'))


@auth_bp.route('/admin/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password  = request.form.get('current_password', '')
        new_password      = request.form.get('new_password', '')
        confirm_password  = request.form.get('confirm_password', '')

        if not check_password_hash(current_user.password, current_password):
            flash('Current password is incorrect', 'error')
            return render_template('admin/change_password.html')

        if new_password != confirm_password:
            flash('New passwords do not match', 'error')
            return render_template('admin/change_password.html')

        is_valid, message = validate_password_strength(new_password)
        if not is_valid:
            flash(message, 'error')
            return render_template('admin/change_password.html')

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
