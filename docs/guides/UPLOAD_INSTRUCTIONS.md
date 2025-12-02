# Upload Your Django Project to Oracle Cloud

You have 3 options to upload your project to the server:

## Option 1: Using SCP from Your Local Machine (Recommended)

### Windows (using WinSCP):
1. Download WinSCP: https://winscp.net/
2. Connect using:
   - Host: YOUR_PUBLIC_IP
   - Username: ubuntu
   - Private key: Your downloaded .key file
3. Navigate to `/home/ubuntu/attendance-system/`
4. Upload ALL your project files:
   - manage.py
   - attendance_system/ folder
   - core/ folder
   - db.sqlite3
   - requirements.txt
   - All other files and folders

### Mac/Linux (using command line):
```bash
# From your local machine, in your project directory
scp -i ~/path/to/your-key.key -r * ubuntu@YOUR_PUBLIC_IP:/home/ubuntu/attendance-system/
```

## Option 2: Using Git (If you have GitHub)

```bash
# On your Oracle Cloud instance
cd ~/attendance-system
git clone https://github.com/yourusername/your-repo.git .
```

## Option 3: Create a ZIP and Upload

```bash
# On your local machine
zip -r attendance-system.zip attendance_system core manage.py db.sqlite3 requirements.txt

# Upload the zip
scp -i ~/path/to/your-key.key attendance-system.zip ubuntu@YOUR_PUBLIC_IP:~/

# On Oracle instance
cd ~/attendance-system
unzip ~/attendance-system.zip
```

---

## After Upload:

1. **Update settings.py for production:**
```bash
cd ~/attendance-system
source venv/bin/activate
nano attendance_system/settings.py
```

Add/modify these lines:
```python
import os

SECRET_KEY = 'your-secret-key-change-this-in-production'
DEBUG = False
ALLOWED_HOSTS = ['YOUR_PUBLIC_IP', 'localhost']

# SQLite database (already configured, just verify)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

2. **Run migrations and collect static files:**
```bash
python manage.py migrate
python manage.py create_initial_data
python manage.py collectstatic --noinput
```

3. **Configure Gunicorn and Nginx:**
```bash
bash configure_services.sh
```

4. **Access your app:**
```
http://YOUR_PUBLIC_IP
```

Login with:
- Username: root
- Password: root123

---

## Troubleshooting:

**If you get permission errors:**
```bash
sudo chown -R ubuntu:ubuntu ~/attendance-system
chmod +x manage.py
```

**If database is locked:**
```bash
chmod 664 db.sqlite3
sudo chown ubuntu:www-data db.sqlite3
```

**To restart services:**
```bash
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

**To view logs:**
```bash
sudo journalctl -u gunicorn -f
```
