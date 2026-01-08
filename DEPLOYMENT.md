# Deployment Guide for Social Project

## Prerequisites

1. Python 3.8+
2. PostgreSQL (for production)
3. Redis (for caching and sessions)
4. Web server (Nginx recommended)

## Environment Setup

1. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Configure environment variables in `.env`:**
   ```env
   SECRET_KEY=your-super-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   DATABASE_URL=postgres://user:password@localhost:5432/social_db
   REDIS_URL=redis://127.0.0.1:6379/1
   EMAIL_HOST=smtp.gmail.com
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ADMIN_EMAIL=admin@yourdomain.com
   ```

## Database Setup

1. **Create PostgreSQL database:**
   ```sql
   CREATE DATABASE social_db;
   CREATE USER social_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE social_db TO social_user;
   ```

2. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

## Static Files

1. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

## Production Server Setup

### Using Gunicorn

1. **Install Gunicorn:**
   ```bash
   pip install gunicorn
   ```

2. **Create Gunicorn configuration (`gunicorn.conf.py`):**
   ```python
   bind = "127.0.0.1:8000"
   workers = 3
   worker_class = "sync"
   worker_connections = 1000
   max_requests = 1000
   max_requests_jitter = 100
   timeout = 30
   keepalive = 2
   preload_app = True
   ```

3. **Start Gunicorn:**
   ```bash
   gunicorn --config gunicorn.conf.py social_project.wsgi:application
   ```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    location /static/ {
        alias /path/to/your/project/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /path/to/your/project/media/;
        expires 1y;
        add_header Cache-Control "public";
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Maintenance

### Data Cleanup

Run the cleanup command regularly:
```bash
python manage.py cleanup_data --days=90
```

### Backup Database

```bash
pg_dump social_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Monitor Logs

```bash
tail -f /var/log/django/social_project.log
```

## Security Checklist

- [ ] SECRET_KEY is unique and secure
- [ ] DEBUG is False in production
- [ ] ALLOWED_HOSTS is properly configured
- [ ] Database credentials are secure
- [ ] SSL/HTTPS is enabled
- [ ] Regular security updates are applied
- [ ] File upload limits are configured
- [ ] Rate limiting is implemented (if needed)

## Performance Optimization

1. **Enable Redis caching**
2. **Use CDN for static files**
3. **Optimize database queries**
4. **Monitor application performance**
5. **Regular database maintenance**

## Troubleshooting

### Common Issues

1. **Static files not loading:**
   - Check STATIC_ROOT and STATIC_URL settings
   - Run `collectstatic` command
   - Verify Nginx configuration

2. **Database connection errors:**
   - Check DATABASE_URL format
   - Verify PostgreSQL is running
   - Check user permissions

3. **Email not working:**
   - Verify EMAIL_* settings
   - Check firewall rules for SMTP
   - Test with Django shell

### Logs Location

- Application logs: `/var/log/django/social_project.log`
- Nginx logs: `/var/log/nginx/access.log` and `/var/log/nginx/error.log`
- PostgreSQL logs: `/var/log/postgresql/`