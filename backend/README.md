# Zimna Backend

Zimna is an AI-powered life planning and goal management platform designed to help users turn long-term goals into clear, actionable steps.

This repository contains the backend service for Zimna, built with Django and Django REST Framework. It provides REST APIs for authentication, goal management, task planning, scheduling, and AI-powered features.

---

## 🚀 Features

- User authentication and authorization
- Goal creation and management with AI-powered SMART goal breakdown
- Task generation and tracking
- Smart planning and scheduling using Google Gemini AI
- Progress tracking
- PostgreSQL database integration
- CORS support for frontend integration

---

## 🛠 Tech Stack

- **Python** - Backend language
- **Django** - Web framework
- **Django REST Framework** - API framework
- **PostgreSQL** - Database
- **Google Generative AI (Gemini)** - AI for goal decomposition
- **JWT Authentication** (planned)
- **Docker** - Containerization

---

## 📂 Project Structure

```
zimna-backend/
│
├── config/                 # Main Django project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py         # Django settings with PostgreSQL and AI config
│   ├── urls.py             # Main URL configuration
│   ├── views.py
│   └── wsgi.py
│
├── goals/                  # Goal management app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py           # Goal model with user relationships
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py             # Goal API endpoints
│   ├── views.py            # Goal views including AI decomposition
│   ├── management/
│   │   └── commands/
│   │       └── smartify.py # Management command for AI goal processing
│   └── migrations/         # Database migrations
│
├── tasks/                  # Task management app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py           # Task model linked to goals
│   ├── serializers.py
│   ├── tests.py
│   ├── views.py
│   └── migrations/
│
├── users/                  # Custom user management app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py           # Custom User model with email auth
│   ├── serializers.py
│   ├── tests.py
│   ├── views.py
│   └── migrations/
│
├── workflow/               # AI workflow module
│   ├── __init__.py
│   └── ai_engine.py        # Google Gemini integration for goal processing
│
├── templates/              # HTML templates
│   └── test.html
│
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
├── memory_test.py          # Memory testing script
└── README.md               # This file
```

---

## ⚙️ Local Development Setup

Follow the steps below to set up the backend locally.

### Prerequisites

- Python 3.8+
- PostgreSQL database
- Google Gemini API key

### 1. Clone and Navigate to Project Directory

```bash
git clone <repository-url>
cd zimna-backend
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the project root with the following variables:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
PGHOST=localhost
PGDATABASE=zimna_db
PGUSER=your_db_user
PGPASSWORD=your_db_password
PGPORT=5432

# AI Configuration
GEMINI_API_KEY=your-google-gemini-api-key
```

### 4. Database Setup

Ensure PostgreSQL is running and create the database:

```bash
createdb zimna_db
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

### 8. Test AI Functionality

You can test the AI goal decomposition using the management command:

```bash
python manage.py smartify "I want to learn Python and build a web app"
```

---

## 🐳 Docker Setup (Alternative)

If you prefer using Docker:

```bash
# Build the image
docker build -t zimna-backend .

# Run the container
docker run -p 8000:8000 --env-file .env zimna-backend
```

---

## 📡 API Endpoints

### Goals API

- `POST /api/decompose/` - Decompose user input into SMART goals and tasks using AI

### Authentication

- Basic authentication is currently implemented
- JWT authentication planned for future releases

### Admin Interface

- Access Django admin at `http://localhost:8000/admin/`

---

## 🧪 Testing

Run tests for all apps:

```bash
python manage.py test
```

---

## 📈 Roadmap

### Phase 1 — Core Backend (Current)

- ✅ User authentication
- ✅ Goals API with AI decomposition
- ✅ Task management
- ✅ PostgreSQL integration
- ✅ Google Gemini AI integration
- Basic planner functionality

### Phase 2 — Intelligence (In Progress)

- Enhanced AI task breakdown
- Smart rescheduling
- Productivity profiling
- Advanced analytics

### Phase 3 — Platform (Planned)

- JWT authentication
- Team collaboration
- Accountability features
- Analytics dashboard
- Mobile app API

---

## 🤝 Contribution

This project is currently under active development. Feedback, issues, and suggestions are welcome.

### Development Guidelines

1. Follow Django best practices
2. Write tests for new features
3. Use meaningful commit messages
4. Update documentation for API changes

---

## 📄 License

This project is private and proprietary. All rights reserved.

---

## ✨ Author

Built by Jesse Adesina as part of Zimna AI platform.
