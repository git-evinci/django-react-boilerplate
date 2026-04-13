
# 🚀 Django-React Modern Stack Boilerplate

A professional, opinionated boilerplate designed to jumpstart web applications. This repository provides a high-performance starting point by bridging a **Django REST Framework** backend with a **Vite-powered React** frontend.

## 🛠 Tech Stack

### Backend (Django)
* **Framework:** [Django 5.x](https://www.djangoproject.com/)
* **API:** [Django REST Framework (DRF)](https://www.django-rest-framework.org/)
* **Package Manager:** [Poetry](https://python-poetry.org/) 
* **Admin UI:** [Django Unfold](https://github.com/unfoldadmin/django-unfold) (Modern Tailwind-based Admin)
* **Async Tasks:** Celery + Celery Beat (Ready)
* **Testing:** Pytest

### Frontend (React)
* **Build Tool:** [Vite](https://vitejs.dev/)
* **Library:** [React](https://react.dev/)
* **Styling:** [Tailwind CSS](https://tailwindcss.com/)

---

## 📁 Project Structure

```text
.
├── backend/                # Django Project Root
│   ├── core/               # Main Application Domain
│   │   ├── admin/          # Modular Admin (User, dashboard, celery)
│   │   ├── models/         # Modular Models (Base, User)
│   │   ├── settings/       # Split Settings (Dev, Prod, Logging)
│   │   ├── static/         # Global assets
│   │   └── templates/      # Base HTML & Vite layouts
│   └── manage.py
├── frontend/               # Vite + React Project
├── scripts/                # DevOps & Cleanup Utilities
├── tests/                  # Pytest Suite
├── pyproject.toml          # Poetry Configuration
└── README.md
```