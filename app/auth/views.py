from flask import render_template, redirect, request, url_for, flash, session
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import auth
from .forms import LoginForm, RegistrationForm
from ..models import User
from app import db

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = ''
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            session['name'] = user.username
            return redirect(request.args.get('next') or url_for('main.index'))
        error = 'Invalid username or password.'
    return render_template('auth/login.html', form=form, error=error)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session['name'] = ''
    session['room'] = ''
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
        username=form.username.data,
        password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
