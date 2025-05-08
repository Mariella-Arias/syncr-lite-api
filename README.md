# Syncr Lite API

A Django REST Framework backend for a workout tracking application, providing a comprehensive set of APIs for workout management, scheduling, and activity tracking.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
  - [Authentication](#authentication)
  - [Workouts](#workouts)
  - [Exercises](#exercises)
  - [Activity](#activity)
- [Setup and Installation](#setup-and-installation)
- [Development](#development)
- [Container Architecture](#container-architecture)

## Overview

This API serves as the backend for a workout tracking application, allowing users to create custom workouts, schedule them, and track their fitness progress. Built with Django and Django REST Framework, it follows RESTful design principles and includes JWT-based authentication.

## Features

- **User Management**: Registration, authentication, password management
- **Workout Templates**: Create and manage reusable workout templates
- **Exercise Library**: Access to standard exercises and ability to create custom ones
- **Workout Scheduling**: Plan workouts on a calendar
- **Activity Tracking**: Record completed workouts and view history

## Project Structure

```
api_service/
│
├── api_service/         # Main Django project
│   ├── settings.py      # Project settings
│   ├── urls.py          # Main URL routing
│   └── wsgi.py          # WSGI configuration
│
├── accounts/            # User management app
│   ├── models.py        # User models
│   ├── views.py         # Authentication views
│   ├── serializers.py   # User serializers
│   └── urls.py          # Auth URL patterns
│
├── workouts/            # Workout management app
│   ├── models.py        # Workout and exercise models
│   ├── views.py         # API views
│   ├── serializers.py   # Data serializers
│   └── urls.py          # Workout URL patterns
│
├── Dockerfile           # Docker configuration
├── compose.yml          # Docker Compose configuration
├── requirements.txt     # Python dependencies
└── manage.py            # Django management script
```

## Technology Stack

- **Framework**: Django 5.1+ & Django REST Framework 3.15+
- **Database**: PostgreSQL 12+
- **Authentication**: Djoser 2.3+ & SimpleJWT 5.4+
- **Containerization**: Docker & Docker Compose
- **Additional Libraries**:
  - psycopg2 2.9+
  - python-dotenv 1.0+

## API Documentation

### Authentication

Authentication is implemented using Djoser and SimpleJWT for secure JWT-based token management.

| Endpoint                              | Method | Description                  |
| ------------------------------------- | ------ | ---------------------------- |
| `/auth/users/`                        | POST   | Register new user            |
| `/auth/users/activation/`             | POST   | Activate user account        |
| `/auth/token/`                        | POST   | Login and receive JWT tokens |
| `/auth/token/refresh/`                | POST   | Refresh access token         |
| `/auth/users/reset_password/`         | POST   | Request password reset       |
| `/auth/users/reset_password_confirm/` | POST   | Complete password reset      |
| `/auth/users/set_password/`           | POST   | Change password              |
| `/auth/users/me/`                     | GET    | Get current user info        |
| `/auth/users/me/`                     | DELETE | Delete account               |
| `/api/token/blacklist/`               | POST   | Logout (token blacklisting)  |

### Workouts

Endpoints for managing workout templates.

| Endpoint          | Method | Description                  |
| ----------------- | ------ | ---------------------------- |
| `/workouts/`      | GET    | List all workouts            |
| `/workouts/`      | POST   | Create new workout           |
| `/workouts/<id>/` | GET    | Get specific workout details |
| `/workouts/<id>/` | PUT    | Update workout               |
| `/workouts/<id>/` | DELETE | Delete workout               |

### Exercises

Endpoints for exercise management.

| Endpoint                    | Method | Description            |
| --------------------------- | ------ | ---------------------- |
| `/workouts/exercises/`      | GET    | List all exercises     |
| `/workouts/exercises/`      | POST   | Create custom exercise |
| `/workouts/exercises/<id>/` | DELETE | Delete custom exercise |

### Activity

Endpoints for scheduling and tracking workout activity.

| Endpoint                   | Method | Description                                | Parameters/Query Parameters                                                                                                                    |
| -------------------------- | ------ | ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `/workouts/activity/`      | GET    | View scheduled activities                  | **Query Parameters**:<br>`type`: all (default), recent, period<br>`start_date`: YYYY-MM-DD (for period)<br>`end_date`: YYYY-MM-DD (for period) |
| `/workouts/activity/`      | POST   | Schedule a workout                         | **Required Body**:<br>`workout`: workout_id (integer)<br>`date_scheduled`: YYYY-MM-DD                                                          |
| `/workouts/activity/<id>/` | PATCH  | Update activity (reschedule/mark complete) | **Optional Body**:<br>`date_scheduled`: YYYY-MM-DD<br>`completed`: boolean                                                                     |
| `/workouts/activity/<id>/` | DELETE | Remove scheduled activity                  | N/A                                                                                                                                            |

## Setup and Installation

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd syncr-lite-api
   ```

2. Set up secret files:

   ```bash
   # Email credentials
   cp email/password.txt.example email/password.txt
   # Edit email/password.txt with your email password

   # Database credentials
   cp db/password.txt.example db/password.txt
   # Edit db/password.txt with your database password

   # Server secret key
   cp server/secretkey.txt.example server/secretkey.txt
   # Edit server/secretkey.txt with your Django secret key
   ```

3. Build and start the containers:

   ```bash
   docker compose up --build
   ```

4. Run migrations:

   ```bash
   docker compose exec server python manage.py makemigrations  # if needed
   docker compose exec server python manage.py migrate
   ```

5. Create superuser (optional):
   ```bash
   docker compose exec server python manage.py createsuperuser
   ```

## Development

### Daily Development Workflow

```bash
# Start services (with auto-reload on code changes)
docker compose up

# View logs
docker compose logs -f server

# Stop services
docker compose down
```

## Container Architecture

The application uses Docker Compose with the following features:

- PostgreSQL configured as a dependent service
- Database healthchecks to ensure service readiness
- Named volumes for data persistence
- Non-privileged user for application container
- Secrets management for environment variables (no .env files)
- Development watch mode for auto-reload during development

## Security

The application implements several security measures:

- JWT authentication with HTTP-only cookies
- Token refresh and blacklisting mechanisms
- Email verification for account registration
- Secure password hashing and reset flow
- CSRF protection
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- Non-privileged Docker containers

## Authentication Flow

1. User registers with email, name, and password
2. System sends activation email
3. User activates account via email link
4. User logs in to receive JWT tokens (stored as HTTP-only cookies)
5. Access token is used for API calls (valid for 5 minutes)
6. Refresh token is used to obtain new access tokens when needed
7. On logout, tokens are blacklisted
