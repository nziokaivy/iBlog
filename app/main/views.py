import os
import secrets
from flask_wtf import FlaskForm
from flask import Flask, render_template, url_for, flash, redirect, request, abort
from . import main
from ..requests import get_quotes
from ..models import User, Post, Quote, Subscribe
from flask_login import login_user,logout_user,login_required, current_user
from .forms import UpdateProfileForm, PostForm, SubscribeForm
from ..import db, photos
from flask_wtf import Form
from wtforms import Form, TextField, BooleanField, PasswordField, TextAreaField, validators

@main.route('/')
def index():
    random_quotes = get_quotes()
    print(random_quotes)
    title = 'Home'
    return render_template('index.html', title = title, quotes = random_quotes)



@main.route("/home")
def home():
    posts = Post.query.order_by(Post.date_posted.desc())
    return render_template('home.html', posts=posts)

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

@main.route('/post/new', methods= ['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!','success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html',title="New Post", form=form, legend='New Post')  

@main.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', id=post_id, title=post.title, post=post)


@main.route("/post/<int:post_id>/update", methods= ['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()  
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('main.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content


    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@main.route("/post/<int:post_id>/delete", methods= ['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first() 
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'success')
    
    return redirect(url_for('main.home'))

@main.route('/<int:post_id>/add/comment', methods=['GET', 'POST'])
def comment(post_id):
    post = Post.query.filter_by(id = post_id).first()
    form = CommentForm()

    if form.validate_on_submit():
        body = form.body.data
        author = form.author.data

        new_comment = Comment(body=form.body.data, post=post, author=acurrent_user)
        new_comment.save_comment()
        flash('Your comment has been published.')
        return redirect(url_for('main.post', id=post.id ))
    
    return render_template('main.comments.html', comments=comments, post=post)


@main.route('/<int:post_id>/comments')
def show_comments(post_id):
    post = Post.query.filter_by(id = post_id).first()
    comments = Comment.get_comments(id)
    
    return render_template('main.show_comments.html', comments=comments, post=post)

@main.route('/subscribe',methods=["GET","POST"])
def subscribe():
    form = SubscribeForm()
    if form.validate_on_submit():
        subscriber = Subscribe(name=form.name.data,email=form.email.data)
        db.session.add(subscriber)
        db.session.commit()

        mail_message("Welcome to iBlog","email/subscribe_user",subscriber.email,subscriber=subscriber)
        
        return redirect(url_for('main.home'))
    return render_template('subcribe.html',subscribe_form=form)    