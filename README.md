# Django File Manager

Django File Manager is a web application built with Django that allows users to manage files and download them. It includes features such as user authentication, file listing, downloading, and logging download activities.

## Features

- User authentication using JWT (JSON Web Tokens).
- File listing and downloading functionality.
- Soft delete functionality to mark files as deleted without removing them from the database.
- Logging download activities to track which users download which files.

## Installation

1. **After clone, Install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Run migrations to set up the database:**

```bash
python manage.py migrate
```

3. **Run Celery worker and beat:**

```bash
celery -A ftp_service worker --loglevel=info
celery -A ftp_service beat --loglevel=info

```

4. **Start the development server:**
```bash
python manage.py runserver
```


## Usage

1. Access the web application by visiting http://localhost:8000 in your web browser.
2. Log in with your credentials or register for a new account if you don't have one.
3. Once logged in, you can view the list of files, download files, and see your download history.