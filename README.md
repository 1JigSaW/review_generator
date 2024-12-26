
# Django Project Setup Guide

This is a Django project. Follow the steps below to set up and run the project locally.

---

## Requirements

- Python 3.10+
- pip (Python package manager)
- Virtual Environment tool (e.g., `venv`)

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd <project-folder>
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root directory and add the required variables. Use `.env.example` as a reference.

Example `.env`:
```plaintext
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
SERVICE=name-of-service (company, product, app)
```

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Run the server

```bash
python manage.py runserver
```

The server will be available at `http://127.0.0.1:8000`.
