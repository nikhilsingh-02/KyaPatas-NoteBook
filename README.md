# KyaPata Notebook 📝

A simple, secure, and stylish personal note-taking web application built with Flask.

---

## ## About The Project

**KyaPata Notebook** is a full-stack web application that allows users to securely register, log in, and manage their personal notes. It provides a clean, dark-themed interface for creating, viewing, updating, and deleting notes, ensuring that each user's notes are private and accessible only to them.

This project was built to demonstrate core concepts in web development, including user authentication, database interactions, and front-end design using a back-end framework.

---

## ## Key Features

* **Secure User Authentication**: Full registration and login system. Passwords are securely hashed using **Bcrypt**.
* **CRUD Functionality**: Users can **C**reate, **R**ead, **U**pdate, and **D**elete their own notes.
* **Session Management**: Uses Flask-Login to manage user sessions, keeping users logged in across requests.
* **Private Notes**: Notes are tied to individual user accounts, so you can only see the notes you create.
* **Task Tracking**: Notes can be marked as 'Completed' or 'Uncompleted' and can be filtered.
* **Clean UI**: A modern, responsive, dark-themed interface built with basic HTML/CSS.

---

## ## Tech Stack

This project is built with the following technologies:

* **Backend**: ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
* **Database**: ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white) with **SQLAlchemy** (ORM)
* **Authentication**: Flask-Login, Flask-Bcrypt
* **Frontend**: HTML5, CSS3, Jinja2

---

## ## Getting Started

To get a local copy up and running, follow these simple steps.

### ### Prerequisites

Make sure you have **Python 3.6+** and **Git** installed on your system.

### ### Installation

1.  **Clone the repository**
    ```sh
    git clone [https://github.com/your-username/KyaPatas-Notebook.git](https://github.com/your-username/KyaPatas-Notebook.git)
    cd KyaPatas-Notebook
    ```

2.  **Create and activate a virtual environment**
    * This keeps your project dependencies isolated.

    ```sh
    # Create the environment
    python -m venv venv

    # Activate on Windows
    venv\Scripts\activate

    # Activate on macOS/Linux
    source venv/bin/activate
    ```

3.  **Install the required packages**
    * This project uses a `requirements.txt` file to manage dependencies. To install them, run:
    ```sh
    pip install -r requirements.txt
    ```
    * (If you add new packages, remember to update the file by running `pip freeze > requirements.txt`)

4.  **Run the application**
    ```sh
    python app.py
    ```

5.  **View the app**
    * Open your web browser and navigate to: `http://127.0.0.1:5000`

---

## ## Project Structure
