from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from . import db, mail, flask_app
from .models import User, Order, Products, Comment
from random import randint

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['GET', 'POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        flash('User not exists.')
        return redirect(url_for('auth.login'))

    if not check_password_hash(user.password_hash, password):
        flash('Wrong password')
        return redirect(url_for('auth.login'))

    login_user(user)

    return redirect(url_for('app.index'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists.')
        return redirect(url_for('auth.signup'))

    new_user = User(
        email=email,
        password_hash=generate_password_hash(password, method='sha256'),
        wallet=100.,
        admin=False
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('app.index'))


@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    try:
        orders = Order.query.filter_by(user_id=current_user.id).all()
        if request.method == "POST":
            amount = request.form['amount']
            current_user.wallet += float(amount)
            db.session.commit()
        return render_template('profile.html', current_user=current_user, orders=orders, Products=Products,
                               Comments=Comment)
    except:
        return render_template('error.html')


@auth.route('/change_email_address', methods=['GET', 'POST'])
@login_required
def change_email_address():
    try:
        new_email = request.form.get('email')
        if request.method == "POST":
            if request.form.get('verify-code') != str(current_user.verify_code):
                flash("Incorrect verification code")
                return redirect(url_for('auth.change_email_address'))
            elif current_user.email == new_email:
                flash("New email address could not be same as the old one")
                return redirect(url_for('auth.change_email_address'))
            elif not new_email:
                flash("Email address could not be empty")
                return redirect(url_for('auth.change_password'))
            else:
                current_user.verify_code = randint(10000, 99999)
                current_user.email = new_email
                db.session.commit()
                return redirect(url_for('auth.profile'))
        else:
            return render_template('change_email_address.html', curr_email=current_user.email)
    except:
        return render_template('error.html')


@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    try:
        if request.method == "POST":
            old_password = request.form.get('old_password')
            new_password = request.form.get('new_password')
            if request.form.get('verify-code') != str(current_user.verify_code):
                flash("incorrect verification code")
                return redirect(url_for('auth.change_email_address'))
            elif not check_password_hash(current_user.password_hash, old_password):
                flash("Wrong password")
                return redirect(url_for('auth.change_password'))
            elif not new_password:
                flash("Password could not be empty")
                return redirect(url_for('auth.change_password'))
            elif check_password_hash(current_user.password_hash, new_password):
                flash("New password Could not be same as the old one")
                return redirect(url_for('auth.change_password'))
            else:
                current_user.verify_code = randint(10000, 99999)
                current_user.password_hash = generate_password_hash(new_password, method='sha256')
                db.session.commit()
                return redirect(url_for('auth.profile'))
        else:
            return render_template('change_password.html')
    except:
        return render_template('error.html')


@auth.route('/send_mail')
def send_mail():
    current_user.verify_code = randint(1000, 9999)
    db.session.commit()
    msg = Message("Email Verification", sender=flask_app.config["MAIL_USERNAME"], recipients=[current_user.email])
    msg.body = 'This is your verification code: ' + str(current_user.verify_code)
    mail.send(msg)
    return redirect(url_for('auth.change_password'))
