from flask import redirect, url_for, flash, render_template, request
from flask_login import current_user, login_required, logout_user, login_user

from app import db
from app.auth import auth
from app.auth.forms import SignUpForm, LoginForm, PasswordResetForm, RenewPasswordForm, ChangePasswordForm
from app.main.email import send_mail
from app.main.forms import SearchForm
from app.model import User


# Pass function to navbar, required for search form to use CSRF token
@auth.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


# Checks if current user is unconfirmed and redirects to unconfirmed page
@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


# Login page contains form and queries email address and verifies password
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect if already logged in
    if current_user.is_authenticated:
        flash('You are currently logged in ' + current_user.username)
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        # Query database for email from form
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            # If password is correct the user is logged in
            login_user(user, form.remember_me.data)
            return redirect(url_for('main.index'))
        # If either password or email is wrong the same message is displayed
        flash('Invalid email or password.')
    return render_template('auth/login.html', form=form)


# Logout user
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        flash('You are currently logged in ' + current_user.username)
        return redirect(url_for('main.index'))

    form = SignUpForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_mail(user.email, 'Confirm Your Account',
                  'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to your email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html', form=form)


# Unconfirmed page reminds user to confirm email and offers link to resend token
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


# Resend token to confirm email
@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_mail(current_user.email, 'Confirm Your Account',
              'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


# Checks valid token and updated database with new confirmed status
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account.')
    else:
        flash('The confirmation link is invalid or expired.')
    return redirect(url_for('main.index'))


# Sends password reset token to users email
@auth.route('/password-reset', methods=['GET', 'POST'])
def password_reset():
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None:
            token = user.generate_password_reset_token()
            send_mail(user.email, 'Reset your password',
                      'auth/email/password-reset', user=user, token=token)
        flash('If your email is registered a password reset link has been sent to that address.')
        return redirect(url_for('auth.login'))
    return render_template('auth/password-reset.html', form=form)


# Checks valid reset token and updated users new password in database
@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = RenewPasswordForm()
    if form.validate_on_submit():
        if User.confirm_password_reset(token=token, new_password=form.password.data):
            db.session.commit()
            flash('Password reset successful.')
            return redirect(url_for('auth.login'))
        else:
            flash('Token expired or invalid. Password reset failed.')
            return redirect(url_for('main.index'))
    return render_template('auth/renew-password.html', form=form)


# Allows user to change password once verified current password
@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = current_user
        if user is not None and user.verify_password(form.old_password.data):
            user.password = form.new_password.data
            db.session.add(user)
            db.session.commit()
            flash('Your password has been changed.')
            return redirect(url_for('main.index'))
        else:
            flash('Incorrect current password.')
    return render_template('auth/change-password.html', form=form)





