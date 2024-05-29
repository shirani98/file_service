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

4. **Set default data:**
In this step, you should set default data like login data or FTP IP in the client file, sync files, and tasks file. search # Change_data in project to find Changeable data.


5. **Start the development server:**
```bash
python manage.py runserver
```

6. **Add permission run to bash script:**
```bash
chmod +x sync_files.sh
```

7. **Start the Client script:**
```bash
python client.py
```

## Usage

1. Access the web application by visiting http://localhost:8000 in your web browser.
2. Log in with your credentials or register for a new account if you don't have one.
3. you can view the list of files and after login download files.