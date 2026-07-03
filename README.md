#  Expense Tracker - Django Full Stack Project

A full-stack Expense Tracker web application built using **Django, PostgreSQL, Bootstrap, and Chart.js**.  
This project helps users manage daily expenses, track budgets, and visualize monthly spending trends.

---

##  Live Features

-  User Authentication (Register / Login / Logout)
-  Google OAuth Login (Django Allauth)
-  Add / Edit / Delete Expenses (CRUD)
-  Search Expenses by title
-  Filter expenses by Month & Year
-  Monthly Budget Management system
-  Monthly Expense Trend Chart (Chart.js Line Chart)
-  Pagination for better UI experience
-  Responsive UI using Bootstrap
-  PostgreSQL Database integration
-  Django Flash Messages (alerts)

---

## 🛠️ Tech Stack

### Frontend
- HTML
- CSS (Bootstrap)
- JavaScript
- Chart.js

### Backend
- Python
- Django

### Database
- PostgreSQL

### Authentication
- Django Authentication System
- Django Allauth (Google OAuth)

---

## ⚙️ Installation & Setup

 1. Clone Repository

#git clone https://github.com/your-username/Expense_Tracker.git
cd Expense_Tracker

2. Create Virtual Environment & Activate
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Setup PostgreSQL Database
Create a PostgreSQL database
Update credentials inside settings.py

# Google OAuth Setup
Go to Google Cloud Console
Create OAuth Credentials
Add Authorized Redirect URI:
http://127.0.0.1:8000/accounts/google/login/callback/
Add credentials in Django Admin:
- Social Applications → Google
- Client ID
- Secret Key
- Site: example.com

6. Create .env file
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

7. Run Migrations
python manage.py makemigrations
python manage.py migrate

8. Create Superuser
python manage.py createsuperuser

9. Run Server
python manage.py runserver

## Author
Jitendra Kulkarni

LinkedIn: www.linkedin.com/in/jitendra-kulkarni-4992a92b8
