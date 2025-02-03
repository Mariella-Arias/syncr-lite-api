# Syncr Lite API

## Overview

A Django REST Framework backend for a fitness tracking application, providing secure user authentication and workout management capabilities.


## Features

- User Authentication
  - User registration with email verification
  - JWT-based authentication
  - Password reset and management
- Workout Management
  - Create, read, update, and delete workout templates
  - Exercise tracking
- Secure and scalable microservice architecture


## Technology Stack

- Django
- Django REST Framework
- PostgreSQL
- Djoser
- Simple JWT


## Prerequisites
- Python 3.9+ (recommended 3.10 or newer)
- PostgreSQL 12+
- pip
- virtualenv (recommended)

Key Libraries:
- Django 5.1+
- Django REST Framework 3.15+
- Djoser 2.3+
- Simple JWT 5.4+
- psycopg2 2.9+
- python-dotenv 1.0+


## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/fitness-tracker-api.git
cd fitness-tracker-api
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

```bash
# Create PostgreSQL database
createdb fitness_tracker_db

# Configure database settings in settings.py
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

## Running the Server

```bash
python manage.py runserver
```

## Environment Variables

Create a `.env` file with the following:

```
SECRET_KEY=your_secret_key
DEBUG=False
DATABASE_URL=postgres://username:password@localhost/fitness_tracker_db
```

## API Endpoints

- `/auth/users/`: User registration
- `/auth/token/`: JWT token obtain
- `/auth/token/refresh/`: Token refresh
- `/workouts/`: Workout management

## Testing

```bash
python manage.py test
```

## Authentication Flow

1. Register user
2. Verify email
3. Obtain JWT tokens
4. Use tokens for authenticated requests

## Security Features

- JWT authentication
- Email verification
- Password hashing
- CORS protection
- Input validation

## Project Structure

```
api_service/
│
├── api_service/         # Main Django project
│   └── settings.py
│
├── accounts/            # User management app
│   ├── models.py
│   ├── views.py
│   └── serializers.py
│
└── workouts/            # Workout management app
    ├── models.py
    ├── views.py
    └── serializers.py
```
