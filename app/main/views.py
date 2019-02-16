from flask_wtf import FlaskForm
from flask import Flask, render_template, url_for
from . import main
from ..models import User

from flask import render_template,request,redirect,url_for,abort
from . import main
from ..import db
from ..models import User
from flask_login import login_required,current_user
from .. import db

@main.route("/")
@main.route("/home")
def index():
    
    
    return render_template('index.html')
