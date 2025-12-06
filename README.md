# SocialHub 🌐

SocialHub is a simple yet powerful social networking web app built with Django. It allows users to create accounts, share posts, follow others, and interact in a clean, modern interface. Designed with responsive layouts and a light/dark theme toggle, SocialHub delivers a smooth, app-like experience across all devices.

## ✨ Features

-   **User Authentication**: Secure Login and Registration system.
-   **Personalized Feed**: View posts from users you follow and your own updates.
-   **Create Posts**: Share your thoughts with the community.
-   **Interactions**: Like posts and comment on them to engage with others.
-   **Follow System**: Follow other users to see their content in your feed.
-   **Profile Pages**: View user profiles, bios, and their post history.
-   **Dark Mode**: Toggle between light and dark themes for comfortable viewing.
-   **Responsive Design**: Optimized for both desktop and mobile devices.

## 🛠️ Tech Stack

-   **Backend**: Django (Python)
-   **Frontend**: HTML5, CSS3 (Custom Glassmorphism Design)
-   **Database**: SQLite (Default Django DB)

## 🚀 Installation & Run

Follow these steps to set up the project locally:

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/CodeAlpha_SocialHub.git
    cd CodeAlpha_SocialHub/CodeAlpha_SocialHub-main
    ```

2.  **Create a Virtual Environment (Optional but Recommended)**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install django
    ```

4.  **Apply Migrations**
    ```bash
    cd social_project
    python manage.py migrate
    ```

5.  **Run the Server**
    ```bash
    python manage.py runserver
    ```

6.  **Access the App**
    Open your browser and go to: `http://127.0.0.1:8000/`

## 📸 Screenshots

### Home Feed
<img width="1892" height="925" alt="Home Feed" src="screenshots/home_feed.png" />

### Dark Mode
<img width="1895" height="929" alt="Dark Mode" src="screenshots/dark_mode.png" />

### Profile Page
<img width="1891" height="917" alt="Profile Page" src="screenshots/profile_page.png" />

### Login View
<img width="1901" height="909" alt="Login View" src="screenshots/login_view.png" />

### Registration
<img width="1900" height="909" alt="Registration" src="screenshots/registration.png" />

### Create Post
<img width="1914" height="910" alt="Create Post" src="screenshots/create_post.png" />

### Comments
<img width="1919" height="911" alt="Comments" src="screenshots/comments.png" />

### Mobile View
<img width="1900" height="912" alt="Mobile View" src="screenshots/mobile_view.png" />
