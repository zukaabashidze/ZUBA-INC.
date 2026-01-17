from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from models import db, User
from forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check for existing email or username
        if User.query.filter_by(email=form.email.data).first():
            flash('ელ-ფოსტა უკვე გამოყენებულია', 'danger')
            return render_template('register.html', form=form)
        if User.query.filter_by(username=form.username.data).first():
            flash('მომხმარებლის სახელი უკვე გამოყენებულია', 'danger')
            return render_template('register.html', form=form)

        hashed_pw = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('შეცდომა ბაზაში. სცადეთ თავიდან.', 'danger')
            return render_template('register.html', form=form)

        flash('რეგისტრაცია წარმატებულია!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            # safe redirect to next if provided
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('main.dashboard'))
        flash('არასწორი მონაცემები', 'danger')
    return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


