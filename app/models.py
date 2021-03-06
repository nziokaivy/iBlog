from datetime import datetime
from .import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Quote:
  

    def __init__(self,id,author,quote):
        self.id =id
        self.author = author
        self.quote = quote    


class User(db.Model, UserMixin):
     __tablename__ = 'users'
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(20), unique=True, nullable=False)
     email = db.Column(db.String(120), unique=True, nullable=False)
     bio = db.Column(db.String(255))
     image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
     posts = db.relationship('Post', backref='author', lazy=True)
     password_hash = db.Column(db.String(255))
     comments = db.relationship('Comment',backref = 'user',lazy = "dynamic")
 

     @property
     def password(self):
        raise AttributeError('You cannot read the password attribute')

     @password.setter
     def password(self, password):
        self.password_hash = generate_password_hash(password)


     def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
   
     def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comments = db.relationship('Comment',backref = 'post',lazy = "dynamic")
 

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Comment(db.Model, UserMixin):
    __tablename__= 'comments'
     
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.Text)
    author = db.Column(db.Text)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    

    def save_comment(self):
        db.session.add(self)
        db.session.commit()   
    
    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.all()
        Comment.date_posted.desc().filter_by(posts_id=id).all()
        return comments 

    all_comments = [] 

    def __init__(self,body,author):
        self.body = body
        self.author = author

class Subscribe(db.Model):
    __tablename__ = 'subscribe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))

    def __init__(self,name,email):
       self.name = name
       self.email = email    

       def save_subscriber(self):
           db.session.add(self)
           db.session.commit()

    @classmethod
    def get_subscribers(cls):
       subscribers=Subscribe.query.all()
       return subscribers   

if __name__ == '__main__':
    init_db()    