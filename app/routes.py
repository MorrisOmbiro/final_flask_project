from flask import request, Response, render_template, flash, redirect, url_for, make_response, session, g, abort
from app.forms import LoginForm, RegisterForm, PasswordForm, PostForm, CommentForm
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask.json import jsonify
from app.models import *
from app import app, db, bcrypt, csrf
from datetime import datetime
import re
import sys

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except:
        return None

@app.route('/')
def index():
    posts = Post.query.order_by(Post.date_posted.desc())
    users = User.query.order_by(User.id.desc())
    form = PostForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template("main.html", posts=posts, user=User)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('already logged in ')
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            session['username'] = request.form['username']
            flash('logged in')
            return redirect('/')
        else:
            flash('Invalid username or password')
    return render_template("login.html", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash('You may now log in')
        hash_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, password = hash_pwd)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("register.html", form=form, name="Not Reddit")

@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(content=form.img_url.data, title=form.title.data, user_id=current_user.get_id(), date_posted=datetime.now())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('comments', post_id=post.id))
    return render_template("post.html", form=form, name="Not Reddit")

@app.route('/comments/<int:post_id>', methods=['GET', 'POST'])
@login_required
def comments(post_id):
    post = Post.query.filter_by(id=int(post_id)).first_or_404()
    form = CommentForm()
    users_comments = (db.session.query(Post, Comment, User)
         .join(Comment, Comment.post_id == Post.id)
         .join(User, User.id == Comment.user_id)).all()
    if form.validate_on_submit():
        message = form.comment.data
        comment = Comment(user_id=current_user.get_id(), post_id=post.id, message=message, date_posted=datetime.now())
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('comments', post_id=post.id))
    return render_template("comments.html", form=form, post_id=post.id, post=post, users_comments=users_comments)

@app.route('/profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    user = User.query.filter_by(id=int(user_id)).first_or_404()
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('profile.html', posts=posts, user_id=user.id, user=User.query.get(user_id))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out')
    return redirect('/')

@app.route('/vote', methods=['POST'])
@csrf.exempt
def vote():
    if not current_user.is_authenticated:
        return jsonify("false")

    data = request.json
    if not 'up' in data:
        abort(400)

    try:
        post_id = int(data.get('post_id'))
        up = bool(data.get('up'))
    except:
        abort(400)

    post = Post.query.filter_by(id=post_id).first_or_404()

    try:
        post.vote(up)
    except:
        return jsonify(False)

    return jsonify(True)
