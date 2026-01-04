# The Daily Draft 📝  
A modern blogging platform built with Flask and PostgreSQL

---

## 📖 About the Project

**The Daily Draft** is a full-stack blogging application developed using **Flask**, where blog posts are dynamically fetched from a database and rendered for readers.

The platform includes a secure **admin dashboard** for managing blog content and a **contact system** that stores messages in the database while also sending email notifications to the site owner.

Originally developed using **MySQL** with phpMyAdmin (XAMPP), the project was later migrated to **PostgreSQL** due to the lack of reliable lifetime-free MySQL hosting. The PostgreSQL database is hosted on **Neon**, a cloud-native database platform.

The application is deployed on **Vercel** as a serverless Flask app.

---

## 🌐 Live Application

🔗 https://thedailydraft.vercel.app  
*(Custom domain support available via Vercel)*

---

## ✨ Key Features

- 📚 Dynamic blog posts loaded from the database
- 🔐 Secure admin authentication
- 📝 Admin panel for:
  - Creating new blog posts
  - Editing existing posts
  - Deleting posts
- 📩 Contact form:
  - Stores messages in the database
  - Sends email notifications to admin
- 📄 Pagination for blog listing
- 🔒 Environment-based configuration for security
- ☁️ Serverless deployment on Vercel

---

## 🛠️ Technology Stack

**Backend**
- Python
- Flask
- Flask-SQLAlchemy

**Database**
- PostgreSQL (Neon)

**Email**
- Flask-Mail (Gmail SMTP)

**Frontend**
- HTML
- CSS
- Jinja2 Templates

**Deployment**
- Vercel

**Version Control**
- Git & GitHub

---

## 🗄️ Database Architecture

- Initial database: **MySQL (XAMPP / phpMyAdmin)**
- Migrated to: **PostgreSQL**
- Hosting provider: **Neon**

### Why PostgreSQL + Neon?
- No lifetime-free MySQL hosting
- SSL-enabled connections
- Cloud-native and production-ready
- Fully compatible with SQLAlchemy

---

## 📁 Project Structure

```text
FlaskBlogApp/
│
├── app.py              # Main Flask application
├── wsgi.py             # WSGI entry point for deployment
├── config.json         # Application configuration
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (ignored in git)
├── templates/          # HTML templates rendered using Jinja2
├── static/             # Static assets (CSS, images)
└── README.md
