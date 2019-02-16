from flask import render_template,redirect,url_for,flash,request
from . import auth
from flask_login import login_user,logout_user,login_required, current_user
from ..models import User,Post
from .forms import LoginForm,RegistrationForm
from .. import db
# from ..email import mail_message

@auth.route('/register',methods = ["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.username.data}! Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
        title = "New Account"
    return render_template('auth/register.html', title='Register', form = form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and form.password.data:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:    
            flash('Login unsuccessful.Please check email and password!', 'danger')    
        return redirect(url_for('auth.login'))
    return render_template('auth/login.html', title='Login', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out')
    return redirect(url_for("main.index"))

