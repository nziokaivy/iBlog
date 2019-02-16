from flask_wtf import FlaskForm
from flask import Flask, render_template, url_for,redirect, request, abort
from . import main
from ..models import User

from flask import render_template,request,redirect,url_for,abort
from . import main
from ..import db
from ..models import User
from flask_login import login_user,logout_user,login_required, current_user
from .. import db

@main.route("/")
@main.route("/home")
def index():
    
    
    return render_template('index.html')

@main.route("/account")
@login_required
def account():
    
    
    return render_template('account.html', title='Account')

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("account.html", user = user)
