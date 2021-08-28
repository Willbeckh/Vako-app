from app import app
from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegistrationForm, EditProfileForm, UploadPostForm
from app.models import Post, User
from app.models import db
from datetime import datetime


@app.before_request
def before_request():
  """registers the last_seen timestamp of a user"""
  if current_user.is_authenticated:
    current_user.last_seen = datetime.utcnow()
    db.session.commit()


@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html', title='Home')


# login view function
@app.route('/login',  methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated: #deals with a logged in userand blocks the action if user is logged in
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit:
    user = User.query.filter_by(username=form.username.data).first()
    if user and user.check_password(form.password.data):
      flash('Logged in successfully', 'success')
      login_user(user, remember=form.remember_me.data)
      next_page = request.args.get('next')
      return redirect(next_page) if next_page else redirect(url_for('index'))
  return render_template('login.html', title='Sign in', form=form)


# logout function
@app.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('index'))


# registration view function
@app.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash(f"Account for {form.username.data} registered successfully", 'success')
    return redirect(url_for('login'))
  return render_template('register.html', title='Register', form=form)


# user profile section
@app.route('/user_account/<username>')
@login_required
def user_account(username):
  user = User.query.filter_by(username=username).first_or_404()
  posts = Post.query.all()
  return render_template('user_profile.html', title='Profile', user=user, posts=posts)


# edit profile view function
@app.route('/edit_profile', methods=['POST', 'GET'])
@login_required
def edit_profile():
  form = EditProfileForm()
  if form.validate_on_submit():
    current_user.username = form.username.data
    current_user.about_me = form.about_me.data
    db.session.commit()
    flash('Your changes have been saved.')
    return redirect(url_for('user_account', username=current_user.username))
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.about_me.data = current_user.about_me
  return render_template('edit_profile.html', title='Edit Profile', form=form)


# add a blog Post
@app.route('/upload_post', methods=['POST', 'GET'])
@login_required
def upload_post():
  form = UploadPostForm()
  if form.validate_on_submit():
    post = Post(title=form.title.data, body=form.body.data, author=current_user)
    db.session.add(post)
    db.session.commit()
    flash('Your post was successfully published')
    return redirect(url_for('index'))
  return render_template('new_post.html', title='Add blog', legend='New Post', form=form)


# view single post function
@app.route('/post/<int:post_id>')
@login_required
def post(post_id):
  post = Post.query.get_or_404(post_id)
  return render_template('post.html', title=post.title, post=post)


# update post
@app.route('/post/<int:post_id>/update', methods=['POST', 'GET'])
@login_required
def update_post(post_id):
  post = Post.query.get_or_404(post_id)
  if post.author != current_user:
    abort(403)
  form = UploadPostForm()
  if form.validate_on_submit():
    post.title = form.title.data
    post.body = form.body.data
    db.session.commit()
    flash("Your post has been updated!")
    return redirect(url_for('post', post_id=post.id))
  elif request.method == 'GET':
    form.title.data = post.title
    form.body.data =  post.body
  return render_template('new_post.html', title='Update post', legend='Update Post', form=form)


# deleting a post
@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
  post = Post.query.get_or_404(post_id)
  if post.author != current_user:
    abort(403)
  db.session.delete(post)
  db.session.commit()
  flash(f'Your post: `{post.title}` has been Deleted!')
  return redirect(url_for('index'))


# view p0st route
@app.route('/view_post', methods=['GET'])
@login_required
def view_post():
	posts = Post.query.all()
	return render_template('site_posts.html', title='View Posts', posts=posts)