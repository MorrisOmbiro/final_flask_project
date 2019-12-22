from datetime import datetime
from app import db
from flask_login import UserMixin, login_manager, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import enum

class MyEnum(enum.Enum):
    dislikes = 0
    likes = 1
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='commentators', lazy=True)
    votes = db.relationship('Vote', backref='user', lazy=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"User('{self.username}', {self.image_file}')"

class Post(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='comments', lazy=True)
    votes = db.relationship('Vote', backref='post', lazy=True)

    def vote(self, up):
        if not current_user.is_authenticated:
            return

        if up:
            Vote(user=current_user, post=self, like=MyEnum.likes)
        else:
            Vote(user=current_user, post=self, like=MyEnum.dislikes)
        db.session.commit()

    def get_vote(self):
        if not current_user.is_authenticated:
            return None

        try:
            vote = Vote.query.filter_by(post=self, user=current_user).first()
        except:
            return None

        if not vote:
            return None
        if vote.like is MyEnum.likes:
            return True
        else:
            return False


    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    
class Comment(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Vote(db.Model, UserMixin):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)
    like =  db.Column(db.Enum(MyEnum))

