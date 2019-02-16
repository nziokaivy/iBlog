from flask_wtf import FlaskForm
from flask import Flask, render_template, url_for,redirect, request, abort
from . import main
from ..models import User
from flask_login import login_user,logout_user,login_required, current_user
from .forms import UpdateProfile
from ..import db

@main.route("/")
@main.route("/home")
def index():
    
    
    return render_template('index.html')

@main.route("/account")
@login_required
def account():
    
    return render_template('account.html', title='Account')

@main.route('/user/<username>')
def profile(username):
    user = User.query.filter_by(username = username).first()

    if user is None:
        abort(404)

    return render_template('account.html', user = user)

@main.route('/user/<username>/update',methods = ['GET','POST'])
@login_required
def update_profile(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        current_user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.account',username=current_user.username))

    return render_template('update.html',form =form)    
