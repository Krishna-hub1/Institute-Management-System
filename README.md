# Institute-Management-System

A web-based **Institute Management System** built using **Python (Flask)** and **MySQL**.  
This project helps manage institute operations such as student details, attendance, fees, and reports.

---

## 🚀 Features
- Admin authentication (Login / Logout)
- Student management (Add / Update / Delete)
- Course management
- Attendance management
- Fees management
- Reports generation
- Dashboard modules

---

## 🛠️ Technologies Used
- **Python**
- **Flask**
- **MySQL**




## ⚙️ Installation & Setup

### 1) Clone the repository

git clone https://github.com/Krishna-hub1/Institute-Management-System.git
cd Institute-Management-System




2) Install dependencies
pip install -r requirements.txt

 
 Database Setup (MySQL)
 
1) Create Database

Login to MySQL and run:

CREATE DATABASE `Institute Management`;

2) Update MySQL Credentials

Open config.py and update:

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "Institute Management"
}

 Run the Project

Run the application using:

python app.py
