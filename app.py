from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from flask_mail import Mail
import os, math
from dotenv import load_dotenv

# todo - Load environment variables
load_dotenv()

# todo - Load config.json
with open("config.json", "r") as file:
    params = json.load(file)["params"]

# todo - Load credentials from .env
params["admin_username"] = os.getenv("ADMIN_USERNAME")
params["admin_password"] = os.getenv("ADMIN_PASSWORD")
params["gmail-user"] = os.getenv("EMAIL_USER")
params["gmail-password"] = os.getenv("EMAIL_PASSWORD")
params["secret_key"] = os.getenv("SECRET_KEY")

# todo - Neon DB URL
params["prod_uri"] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}?sslmode=require"

# todo - Flask app initialization
app = Flask(__name__)
app.secret_key = params["secret_key"]
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params["gmail-user"],
    MAIL_PASSWORD=params["gmail-password"],
)

mail = Mail(app)

# todo - Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = params["prod_uri"]

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
db = SQLAlchemy(app)

class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone_num = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(25), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tagline = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    img_file = db.Column(db.String(50), nullable=True)

@app.route("/")
def home():
    posts = Posts.query.all()

    # todo - Pagination Logic
    last = math.ceil(len(posts) / int(params["no_of_posts"]))
    page = request.args.get('page', 1, type=int)
    posts = posts[(page - 1)*int(params["no_of_posts"]) : (page - 1)*int(params["no_of_posts"]) + int(params["no_of_posts"])]

    if page == 1:
        prev = "#"
        next = f"/?page={page + 1}"
    elif page == last:
        prev = f"/?page={page - 1}"
        next = "#"
    else:
        prev = f"/?page={page - 1}"
        next = f"/?page={page + 1}"

    return render_template('index.html', params=params, posts=posts, prev=prev, next=next)

@app.route("/about")
def about():
    return render_template('about.html', params=params)

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if 'user' in session and session['user'] == params['admin_username']:
        posts = Posts.query.all()
        return render_template('dashboard.html', params=params, posts=posts)

    if request.method == "POST":
        username = request.form.get('uname')
        userpass = request.form.get('pass')
        if username == params["admin_username"] and userpass == params["admin_password"]:
            session['user'] = username
            posts = Posts.query.all()
            return render_template('dashboard.html', params=params, posts=posts)
    return render_template('login.html', params=params)

@app.route("/edit/<string:sno>", methods=['GET', 'POST'])
def edit(sno):
    if 'user' in session and session['user'] == params['admin_username']:
        if request.method == "POST":
            box_title = request.form.get('title')
            tline = request.form.get('tline')
            slug = request.form.get('slug')
            content = request.form.get('content')
            img_file = request.form.get('img_file')
            date = datetime.now()

            if sno == '0':
                post = Posts(title=box_title, slug=slug, content=content, tagline=tline, img_file=img_file, date=date)
                db.session.add(post)
                db.session.commit()
            else:
                post = Posts.query.get(int(sno))
                post.title = box_title
                post.slug = slug
                post.content = content
                post.tagline = tline
                post.img_file = img_file
                post.date = date
                db.session.commit()
                return redirect(f'/edit/{sno}')
        post = Posts.query.get(int(sno))
        return render_template('edit.html', params=params, post=post, sno=sno)

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect('/dashboard')

@app.route("/delete/<string:sno>", methods=['GET', 'POST'])
def delete(sno):
    if 'user' in session and session['user'] == params['admin_username']:
        post = Posts.query.get(int(sno))
        db.session.delete(post)
        db.session.commit()
    return redirect('/dashboard')

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contact(name=name, email=email, phone_num=phone, message=message, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message(
            f'New Message from {name}',
            sender=email,
            recipients=[params["gmail-user"]],
            body=f"{message}\n{phone}"
        )
        flash("Thanks for submitting your details. We will get back to you soon.", "success")
        return redirect(url_for("contact"))

    return render_template('contact.html', params=params)

@app.route("/post/<string:post_slug>")
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params, post=post)


