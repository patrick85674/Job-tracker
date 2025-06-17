{% load static %}
<div class="hero-image" style="width: 100%; height: 500px; background: url('{% static 'homepage/assets/img/logo_readme.png' %}') no-repeat center center; background-size: cover;">
</div>



A Django-based job tracking website designed to help you manage your job applications effectively.

## Overview

Job Tracker, also known as Jopply, is a website built with Django and Bootstrap 5. It provides an intuitive dashboard for managing your job applications—allowing you to add, edit, delete, and even import application data (via CSV/Excel). The project features user authentication, a responsive user interface, and a FAQ section to help answer common questions.

## Features

- **User Registration and Authentication:** Sign up using your email and password and confirm your account via email.
- **Job Application Management:** Easily add, edit, and delete your job applications.
- **Import Applications:** Import applications from a CSV or Excel file using our provided template.
- **Dashboard:** View a comprehensive list of all your applications, their statuses, and any notes.
- **FAQ Section:** Get quick answers to frequently asked questions regarding the application process and account management.
- **Modern, Responsive UI:** Designed with Bootstrap 5 to ensure a seamless experience across devices.

## Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
- **Database:** Configured with Django’s ORM (SQLite by default)
- **Version Control:** Git

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/patrick85674/Job-tracker.git
   cd Job-tracker
