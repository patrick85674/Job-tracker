<img src="static/homepage/assets/img/logo_readme.png" alt="Logo Readme" style="display: block; width: 100%; height: 200px; object-fit: cover;">








A Django-based job tracking website designed to help you manage your job applications effectively.


## Overview


Job Tracker, also known as Jopply, is a website built with Django and Bootstrap 5. It provides an intuitive dashboard for managing your job applications—allowing you to add, edit, delete and even import application data (via CSV/Excel). The project features user authentication, a responsive user interface and a FAQ section to help answer common questions.


## Features


- **User Registration and Authentication:** Sign up using your email and password and confirm your account via email.
- **Job Application Management:** Easily add, edit, and delete your job applications.
- **Import Applications:** Import applications from a CSV or Excel file using our provided template.
- **Dashboard:** View a comprehensive list of all your applications, their statuses, and any notes.
- **FAQ Section:** Get quick answers to frequently asked questions regarding the application process and account management.
- **Modern, Responsive UI:** Designed with Bootstrap 5 to ensure a seamless experience across devices.


## Tech Stack


- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5, HTMX,
- **Database:** Configured with Django’s ORM (PostgreSQL by default) and MySQL on PythonAnywhere
- **Version Control:** Git


## Installation
1. **Clone the Repository:**
  ```bash
  git clone https://github.com/patrick85674/Job-tracker.git
  cd Job-tracker 
```


2. **Create a Virtual Environment and Activate It:**  
```bash
python3 -m venv .venv
source .venv/bin/activate
  ```
3. **Install Dependencies:**
```bash
pip install -r requirements.txt
```
4. **Set up PostgreSQL or MySQL database** 
Create your database manually (e.g. your_db) in PostgreSQL or MySQL and update the credentials in the .env file.  

5. **Configure the .env file** 
Copy [`sample_env`](./sample_env) to `.env` 
Then fill in required values like:
```bash
SECRET_KEY=your-secret-key
DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432  # or 3306 for MySQL
```
6. **Apply the Migrations:**
```bash
python manage.py migrate
```
7. **Run the Development Server:**
```bash
python manage.py runserver
   ```
8. **Access the Website:**


Open your browser and navigate to http://127.0.0.1:8000


**Usage**  
After the installation steps, register for an account, log in, and start managing your job applications. You can also import your CSV/Excel files and navigate through the dashboard for quick insights.




**License**   
This project is licensed under the MIT License. See the LICENSE file for details.


**Contact**   
For further questions or support, please reach out via email:  jopplyteam@gmail.com
