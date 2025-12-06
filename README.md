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
<img width="1892" height="925" alt="Screenshot 2025-10-18 115125" src="https://github.com/user-attachments/assets/d34a357f-0c7f-4796-95d5-0ace1858634e" />

### Dark Mode
<img width="1895" height="929" alt="Screenshot 2025-10-18 115150" src="https://github.com/user-attachments/assets/40e2ca32-65a8-45c0-9987-46fd8ace7ea0" />

### Profile Page
<img width="1891" height="917" alt="Screenshot 2025-10-18 115218" src="https://github.com/user-attachments/assets/4caa0252-8871-4d51-a5e8-bccc2c70dd50" />

### Login View
<img width="1901" height="909" alt="Screenshot 2025-10-18 115248" src="https://github.com/user-attachments/assets/b550ab69-3f77-4e5a-bf60-e21295f87204" />

### Registration
<img width="1900" height="909" alt="Screenshot 2025-10-18 115434" src="https://github.com/user-attachments/assets/d128031d-a486-4724-94a9-1b4bce01b360" />

### Create Post
<img width="1914" height="910" alt="Screenshot 2025-10-18 115303" src="https://github.com/user-attachments/assets/7304658d-e3d6-480f-85d8-2f8302e32e80" />

### Comments
<img width="1919" height="911" alt="Screenshot 2025-10-18 115319" src="https://github.com/user-attachments/assets/64298c94-83c6-483a-a4a6-d2bb2fda9010" />

### Mobile View
<img width="1900" height="912" alt="Screenshot 2025-10-18 115341" src="https://github.com/user-attachments/assets/0c299cbe-2307-444a-a5d5-e8dd901f4eab" />
