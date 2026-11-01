# KaalPatra (कालपात्र)

> A modern digital chronicle and time-capsule platform for recording, preserving, and revisiting personal or collective milestones.

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1-092E20.svg?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.15-red.svg)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)

---

## 📖 Overview

**KaalPatra** (*काल* = Time, *पात्र* = Document / Vessel / Record) is an application designed to serve as an immutable or scheduled temporal record—allowing users to author chronicles, archive memories, and preserve time-locked reflections.

The project is structured as a decoupled full-stack application with a containerized **Django REST Framework** backend, a **PostgreSQL** persistence layer, and a planned **Next.js** frontend.

---

## 🛠 Tech Stack

- **Backend:**
  - Python 3.12
  - Django 5.1 & Django REST Framework (DRF)
  - `django-cors-headers` (configured for Next.js frontend access)
  - `psycopg2-binary` (PostgreSQL adapter)
  - `python-dotenv`
- **Database:**
  - PostgreSQL 16 Alpine
- **Frontend:**
  - Next.js / React (in `frontend/`, upcoming)
- **DevOps & Containerization:**
  - Docker & Docker Compose

---

## 📂 Project Structure

```text
KaalPatra/
├── backend/
│   ├── chronicles/               # Core chronicles application (models, views, APIs)
│   ├── kaalpatra_core/           # Django project configuration & settings
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── Dockerfile                # Backend container definition
│   ├── manage.py
│   └── requirements.txt          # Python dependencies
├── frontend/                     # Next.js frontend application directory
├── docker-compose.yml            # Multi-container orchestration (Backend + Postgres)
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/)
- *(Optional for bare-metal setup)*: Python 3.12+ and PostgreSQL 16

---

### Option 1: Run with Docker Compose (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd KaalPatra
   ```

2. **Start the containers:**
   ```bash
   docker compose up --build
   ```

3. **Apply database migrations:**
   Open a separate terminal window and run:
   ```bash
   docker compose exec backend python manage.py migrate
   ```

4. **Create a superuser (for Django Admin):**
   ```bash
   docker compose exec backend python manage.py createsuperuser
   ```

5. **Access the application:**
   - **Backend API & Admin:** [http://localhost:8000/admin](http://localhost:8000/admin)
   - **PostgreSQL Database:** `localhost:5432`

---

### Option 2: Local Development Setup (Without Docker)

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Database Environment Variables:**
   Create a `.env` file or export environment variables:
   ```bash
   export DB_NAME=kaalpatra_db
   export DB_USER=kaalpatra_user
   export DB_PASSWORD=kaalpatra_secret_password
   export DB_HOST=localhost
   export DB_PORT=5432
   ```

5. **Run migrations and start dev server:**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

---

## ⚙️ Environment Variables

The backend accepts the following environment variables (defined in `docker-compose.yml` or your local `.env`):

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `DEBUG` | `1` | Enables/disables Django debug mode |
| `DB_NAME` | `kaalpatra_db` | PostgreSQL database name |
| `DB_USER` | `kaalpatra_user` | PostgreSQL user |
| `DB_PASSWORD` | `kaalpatra_secret_password` | PostgreSQL user password |
| `DB_HOST` | `db` (or `localhost`) | Host address of PostgreSQL server |
| `DB_PORT` | `5432` | PostgreSQL port |

---

## 🛣️ Roadmap

- [x] Initialized Django backend with DRF & CORS configuration
- [x] Docker and PostgreSQL 16 containerization
- [ ] Define `Chronicle` models (authoring, timestamping, time-locked reveals, tags)
- [ ] REST API endpoints for managing chronicles and entries
- [ ] Authentication system (Token / JWT authentication)
- [ ] Initialize Next.js frontend with Tailwind CSS
- [ ] Support rich text and media attachments

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
