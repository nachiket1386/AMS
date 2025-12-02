# Complete Deployment Guide

This comprehensive guide covers all deployment options for the Django Attendance Management System.

---

## 📋 Table of Contents

1. [Quick Start Options](#quick-start-options)
2. [Local Development](#local-development)
3. [PythonAnywhere (Easiest)](#pythonanywhere-deployment)
4. [Oracle Cloud (Free Forever)](#oracle-cloud-deployment)
5. [Docker Deployment](#docker-deployment)
6. [Production Best Practices](#production-best-practices)

---

## Quick Start Options

Choose your deployment method based on your needs:

| Method | Difficulty | Cost | Best For |
|--------|-----------|------|----------|
| **PythonAnywhere** | ⭐ Easy | Free | Quick testing, small apps |
| **Oracle Cloud** | ⭐⭐ Medium | Free | Production, full control |
| **Docker** | ⭐⭐⭐ Advanced | Free | Scalability, consistency |
| **Local Dev** | ⭐ Easy | Free | Development only |

---

## Local Development

### Prerequisites
- Python 3.8+
- pip
- Virtual environment

### Setup Steps

```bash
# 1. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 2. Install dependencies
pip install django

# 3. Run migrations
python manage.py migrate

# 4. Create initial data
python manage.py create_initial_data

# 5. Start development server
python manage.py runserver
```

### Access Application
- URL: http://127.0.0.1:8000
- Username: `root`
- Password: `root123`

---

## PythonAnywhere Deployment

**Perfect for: Quick deployment, no server management**

### Step 1: Create Account
1. Go to https://www.pythonanywhere.com
2. Sign up for free account
3. Your subdomain: `username.pythonanywhere.com`

### Step 2: Upload Project

**Via Git:**
```bash
git clone https://github.com/yourusername/attendance-system.git
cd attendance-system
```

**Via Files Tab:**
- Upload ZIP file
- Extract in home directory

### Step 3: Setup Environment

```bash
cd ~/attendance-system
mkvirtualenv --python=/usr/bin/python3.11 attendance-env
pip install django
```

### Step 4: Configure Settings

Edit `attendance_system/settings.py`:
```python
DEBUG = False
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

### Step 5: Run Migrations

```bash
python manage.py migrate
python manage.py create_initial_data
python manage.py collectstatic --noinput
```

### Step 6: Configure Web App

1. Go to **Web** tab
2. Add new web app
3. Manual configuration → Python 3.11
4. Set paths:
   - Source: `/home/username/attendance-system`
   - Virtualenv: `/home/username/.virtualenvs/attendance-env`
5. Edit WSGI file:

```python
import os
import sys

path = '/home/username/attendance-system'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'attendance_system.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

6. Add static files mapping:
   - URL: `/static/`
   - Directory: `/home/username/attendance-system/staticfiles`

### Step 7: Reload & Access

- Click **Reload** button
- Visit: `https://username.pythonanywhere.com`

**Pros:**
- ✅ Easiest setup
- ✅ Free HTTPS
- ✅ No server management

**Cons:**
- ⚠️ Limited CPU time
- ⚠️ 512 MB disk space
- ⚠️ No custom domain (free tier)

---

## Oracle Cloud Deployment

**Perfect for: Production apps, full control, free forever**

### What You Get (Free)
- 4 OCPUs (ARM Ampere)
- 24 GB RAM
- 200 GB storage
- Public IP
- 10 TB bandwidth/month

### Step 1: Create Instance

1. Login to Oracle Cloud Console
2. Create Compute Instance:
   - Name: `attendance-system-vm`
   - Image: Ubuntu 22.04
   - Shape: VM.Standard.A1.Flex (ARM)
   - OCPUs: 2-4
   - Memory: 12-24 GB
   - Public IP: Yes
3. Download SSH keys
4. Note public IP address

### Step 2: Configure Firewall

In Oracle Cloud Console:
1. Go to instance → Subnet → Security List
2. Add Ingress Rules:
   - Port 80 (HTTP)
   - Port 443 (HTTPS)
   - Port 8000 (Django dev - optional)

### Step 3: Connect to Instance

```bash
# Set key permissions
chmod 400 ssh-key.key

# Connect
ssh -i ssh-key.key ubuntu@YOUR_PUBLIC_IP
```

### Step 4: Setup Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install requirements
sudo apt install -y python3 python3-pip python3-venv nginx git

# Configure firewall
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo netfilter-persistent save
```

### Step 5: Upload Project

**Via Git:**
```bash
cd /home/ubuntu
git clone https://github.com/yourusername/attendance-system.git
cd attendance-system
```

**Via SCP (from local machine):**
```bash
scp -i ssh-key.key -r /path/to/project ubuntu@YOUR_PUBLIC_IP:/home/ubuntu/
```

### Step 6: Setup Application

```bash
cd /home/ubuntu/attendance-system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install django gunicorn

# Update settings
nano attendance_system/settings.py
```

Update settings:
```python
DEBUG = False
ALLOWED_HOSTS = ['YOUR_PUBLIC_IP', 'yourdomain.com']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

Run migrations:
```bash
python manage.py migrate
python manage.py create_initial_data
python manage.py collectstatic --noinput
```

### Step 7: Setup Gunicorn Service

```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Add:
```ini
[Unit]
Description=Gunicorn daemon for Django Attendance System
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/attendance-system
Environment="PATH=/home/ubuntu/attendance-system/venv/bin"
ExecStart=/home/ubuntu/attendance-system/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/home/ubuntu/attendance-system/gunicorn.sock \
          attendance_system.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

### Step 8: Setup Nginx

```bash
sudo nano /etc/nginx/sites-available/attendance
```

Add:
```nginx
server {
    listen 80;
    server_name YOUR_PUBLIC_IP;

    location /static/ {
        alias /home/ubuntu/attendance-system/staticfiles/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/attendance-system/gunicorn.sock;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/attendance /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 9: Access Application

Visit: `http://YOUR_PUBLIC_IP`

**Pros:**
- ✅ Free forever
- ✅ Full control
- ✅ Production-ready
- ✅ Powerful hardware

**Cons:**
- ⚠️ Requires server management
- ⚠️ Manual SSL setup

---

## Docker Deployment

**Perfect for: Consistency, scalability, easy updates**

### Prerequisites
- Docker installed
- Docker Compose installed

### Step 1: Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "attendance_system.wsgi:application"]
```

### Step 2: Create docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    command: gunicorn attendance_system.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
    expose:
      - 8000
    environment:
      - DEBUG=False

  nginx:
    image: nginx:latest
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
    ports:
      - "80:80"
    depends_on:
      - web

volumes:
  static_volume:
```

### Step 3: Deploy

```bash
# Build and start
docker-compose up -d --build

# Run migrations
docker-compose exec web python manage.py migrate

# Create initial data
docker-compose exec web python manage.py create_initial_data
```

### Step 4: Access Application

Visit: `http://localhost` or `http://YOUR_SERVER_IP`

**Pros:**
- ✅ Consistent environment
- ✅ Easy updates
- ✅ Portable
- ✅ Scalable

**Cons:**
- ⚠️ Requires Docker knowledge
- ⚠️ Additional layer of complexity

---

## Production Best Practices

### Security

1. **Change SECRET_KEY**
```python
SECRET_KEY = 'your-unique-secret-key-here'
```

2. **Disable DEBUG**
```python
DEBUG = False
```

3. **Set ALLOWED_HOSTS**
```python
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

4. **Use Environment Variables**
```python
import os
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
```

5. **Setup HTTPS**
```bash
# Using Let's Encrypt
sudo certbot --nginx -d yourdomain.com
```

### Database

**For Production, use PostgreSQL:**

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'attendance_db',
        'USER': 'db_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Monitoring

1. **Setup Logging**
```python
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
}
```

2. **Monitor Logs**
```bash
tail -f logs/django.log
```

### Backups

**Daily Database Backup:**
```bash
# SQLite
cp db.sqlite3 backups/db_$(date +%Y%m%d).sqlite3

# PostgreSQL
pg_dump attendance_db > backups/db_$(date +%Y%m%d).sql
```

### Performance

1. **Enable Caching**
2. **Use CDN for static files**
3. **Optimize database queries**
4. **Enable gzip compression**

---

## Troubleshooting

### Common Issues

**502 Bad Gateway**
```bash
sudo systemctl status gunicorn
sudo journalctl -u gunicorn -f
```

**Static Files Not Loading**
```bash
python manage.py collectstatic --noinput
sudo systemctl restart nginx
```

**Database Errors**
```bash
python manage.py migrate
python manage.py check
```

**Permission Errors**
```bash
sudo chown -R ubuntu:www-data /path/to/project
chmod 664 db.sqlite3
```

---

## Support

- Check logs first
- Review error messages
- Consult Django documentation
- Check project README

---

**Choose the deployment method that best fits your needs and technical expertise!**
