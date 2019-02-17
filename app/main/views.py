import os
import secrets
from flask_wtf import FlaskForm
from flask import Flask, render_template, url_for, flash, redirect, request, abort
from . import main
from ..models import User
from flask_login import login_user,logout_user,login_required, current_user
from .forms import UpdateProfileForm
from ..import db, photos

@main.route("/")
@main.route("/home")
def index():
    
    
    return render_template('index.html')

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/pictures', picture_fn)
    form_picture.save(picture_path)

    return picture_fn



@main.route("/account", methods = ['GET','POST'])
@login_required
def account():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = fpicture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('main.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
    image_file = url_for('static', filename='pictures/' + current_user.image_file)
    
    return render_template('account.html', title='Account', image_file=image_file, form=form)

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

    form = UpdateProfileForm()

    if form.validate_on_submit():
        current_user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('account.html',username=current_user.username))

    return render_template('update.html',form =form)  

@main.route('/user/<username>/update/pic',methods= ['POST'])
@login_required
def update_pic(username):
    user = User.query.filter_by(username = username).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.account',username=username))

@main.route('/post/new')
@login_required
def new_post():
     return render_template('create_post.html',title="New Post")  