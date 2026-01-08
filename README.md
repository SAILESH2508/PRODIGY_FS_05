# SocialHub - Enhanced Django Social Media Platform

A modern, feature-rich social media application built with Django, featuring a beautiful glassmorphism UI design and comprehensive social networking functionality.

## 🚀 Features

### Core Features
- **User Authentication & Profiles**
  - User registration, login, logout
  - Profile customization with avatar, bio, location, website
  - User verification badges
  - Password reset functionality

- **Social Networking**
  - Follow/unfollow users
  - Personalized feed based on followed users
  - User search and discovery

- **Posts & Content**
  - Create posts with text and images
  - Image upload with automatic resizing
  - Pin/unpin posts
  - Post deletion (owner only)
  - Character limit with live counter

- **Interactions**
  - Like/unlike posts
  - Comment on posts
  - Reply to comments (nested comments)
  - Real-time like counts

- **Advanced Features**
  - **Hashtags**: Automatic hashtag detection and linking
  - **Mentions**: @username mentions with notifications
  - **Notifications**: Real-time notification system
  - **Search**: Advanced search for users, posts, and hashtags
  - **Pagination**: Efficient content loading

### UI/UX Features
- **Modern Glassmorphism Design**
- **Responsive Layout**
- **Dark Theme with Gradient Backgrounds**
- **Interactive Icons (Ionicons)**
- **Smooth Animations and Transitions**
- **Real-time Notification Badge**

## 🛠️ Technology Stack

- **Backend**: Django 5.2+
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Image Processing**: Pillow
- **UI Framework**: Custom CSS with Glassmorphism design
- **Icons**: Ionicons
- **Forms**: Django Crispy Forms with Bootstrap 5

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd social_project
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Setup
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Load Sample Data (Optional)
```bash
python manage.py populate_db
```

### 8. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

## 🧪 Testing

Run the comprehensive test suite:
```bash
python manage.py test
```

For coverage report:
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

## 🔧 Maintenance

### Data Cleanup
Clean up old notifications and unused hashtags:
```bash
python manage.py cleanup_data --days=90
```

### Database Optimization
The project includes optimized database indexes for better performance. Run migrations to apply:
```bash
python manage.py migrate
```

## 📁 Project Structure

```
social_project/
├── social_app/
│   ├── management/
│   │   └── commands/
│   │       ├── populate_db.py      # Sample data generator
│   │       └── cleanup_data.py     # Data cleanup utility
│   ├── migrations/
│   ├── static/social_app/
│   │   └── css/
│   │       └── style.css           # Glassmorphism styles
│   ├── templates/
│   │   ├── registration/           # Auth templates
│   │   └── social_app/            # App templates
│   ├── templatetags/
│   │   └── social_filters.py      # Custom template filters
│   ├── admin.py                   # Admin configuration
│   ├── forms.py                   # Form definitions
│   ├── models.py                  # Database models
│   ├── tests.py                   # Test suite
│   ├── urls.py                    # URL patterns
│   ├── utils.py                   # Utility functions
│   └── views.py                   # View functions
├── social_project/
│   ├── settings.py                # Django settings
│   ├── settings_production.py    # Production settings
│   └── urls.py                    # Main URL configuration
├── media/                         # User uploads
├── logs/                          # Application logs
├── .env.example                   # Environment template
├── DEPLOYMENT.md                  # Deployment guide
├── requirements.txt               # Python dependencies
└── manage.py                     # Django management script
```

## 🎨 Design System

### Color Palette
- **Primary**: `#8b5cf6` (Violet)
- **Secondary**: `#06b6d4` (Cyan)
- **Accent**: `#f43f5e` (Rose)
- **Background**: Dark gradient with ambient orbs
- **Glass Effects**: Semi-transparent overlays with blur

### Typography
- **Font**: Outfit (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700

## 🔧 Configuration

### Environment Variables
Key environment variables (see `.env.example`):
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: Database connection string
- `EMAIL_HOST_USER`: SMTP email username
- `EMAIL_HOST_PASSWORD`: SMTP email password

### Media Files
Configure media settings in `settings.py`:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Email Backend
For password reset functionality:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Development
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Production
```

### Pagination
Adjust posts per page:
```python
POSTS_PER_PAGE = 10
```

## 🚀 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed production deployment instructions.

### Quick Production Checklist
- [ ] Set environment variables in `.env`
- [ ] Configure PostgreSQL database
- [ ] Set up Redis for caching
- [ ] Configure email backend
- [ ] Set up static file serving
- [ ] Configure logging
- [ ] Set up SSL/HTTPS
- [ ] Run security checks

### Security Features
- Environment-based configuration
- CSRF protection enabled
- XSS protection headers
- Secure file upload handling
- Input validation and sanitization
- SQL injection protection via Django ORM
- Rate limiting ready (can be added)
- Comprehensive logging

## 🔍 Code Quality

### Security Enhancements
- ✅ Secure settings with environment variables
- ✅ Proper exception handling
- ✅ Input validation in forms
- ✅ CSRF protection on AJAX endpoints
- ✅ File upload validation
- ✅ Logging configuration

### Performance Optimizations
- ✅ Database indexes for common queries
- ✅ Query optimization with select_related/prefetch_related
- ✅ Image resizing for uploads
- ✅ Pagination for large datasets
- ✅ Caching configuration ready

### Testing
- ✅ Comprehensive test suite covering models, views, forms, and utilities
- ✅ Test coverage for critical functionality
- ✅ Form validation testing
- ✅ AJAX endpoint testing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your changes
4. Ensure all tests pass (`python manage.py test`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📝 API Endpoints

### Main URLs
- `/` - Home feed
- `/register/` - User registration
- `/login/` - User login
- `/profile/<username>/` - User profile
- `/post/new/` - Create new post
- `/post/<id>/` - Post detail view
- `/hashtag/<name>/` - Hashtag posts
- `/notifications/` - User notifications
- `/search/` - Search functionality

### AJAX Endpoints
- `/post/<id>/like/` - Toggle post like
- `/api/notifications/unread-count/` - Get unread notifications count

## 🐛 Troubleshooting

### Common Issues

1. **Media files not loading**
   - Ensure `MEDIA_URL` and `MEDIA_ROOT` are configured
   - Check URL patterns include media serving

2. **Styles not loading**
   - Run `python manage.py collectstatic`
   - Check `STATIC_URL` configuration

3. **Database errors**
   - Run `python manage.py makemigrations`
   - Run `python manage.py migrate`

4. **Permission errors**
   - Check file permissions for media directory
   - Ensure proper user permissions

5. **Environment variable errors**
   - Ensure `.env` file exists and is properly formatted
   - Check that all required variables are set

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Django framework and community
- Ionicons for beautiful icons
- Google Fonts for typography
- Glassmorphism design inspiration

---

**Built with ❤️ using Django**