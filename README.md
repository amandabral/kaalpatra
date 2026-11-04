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

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
