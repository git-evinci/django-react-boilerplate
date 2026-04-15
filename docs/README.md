# 🚀 Django-React Modern Stack Boilerplate

A professional, opinionated boilerplate designed to jumpstart web applications. This repository provides a high-performance starting point by bridging a **Django REST Framework** backend with a **Vite-powered React** frontend.

## 📑 Table of Contents
- [🚀 Django-React Modern Stack Boilerplate](#-django-react-modern-stack-boilerplate)
  - [📑 Table of Contents](#-table-of-contents)
  - [🛠 Tech Stack](#-tech-stack)
    - [Backend (Django)](#backend-django)
    - [Frontend (React)](#frontend-react)
  - [📁 Project Structure](#-project-structure)
  - [📋 Prerequisites](#-prerequisites)
  - [🚀 Getting Started](#-getting-started)
    - [Step 1: Clone \& Customize](#step-1-clone--customize)
    - [Step 2: Backend \& Environment Setup](#step-2-backend--environment-setup)
    - [Step 3: Database \& Migrations](#step-3-database--migrations)
    - [Step 4: Frontend (React + Tailwind v4)](#step-4-frontend-react--tailwind-v4)
  - [💻 Development](#-development)
    - [Running the Servers](#running-the-servers)
    - [Accessing the Application](#accessing-the-application)
    - [API Documentation (Swagger/Redoc)](#api-documentation-swaggerredoc)
  - [⚠️ Troubleshooting \& Gotchas](#️-troubleshooting--gotchas)
      - [1. `OperationalError: no such table: core_userprofile` (During createsuperuser)](#1-operationalerror-no-such-table-core_userprofile-during-createsuperuser)
      - [2. `django_vite.W001: Cannot read Vite manifest file`](#2-django_vitew001-cannot-read-vite-manifest-file)
      - [3. `unable to open database file`](#3-unable-to-open-database-file)
      - [4. Missing Static Folders Warning (`staticfiles.W004`)](#4-missing-static-folders-warning-staticfilesw004)
      - [5. Blank Swagger UI Page](#5-blank-swagger-ui-page)

---

## 🛠 Tech Stack

### Backend (Django)
* **Framework:** [Django 6.x](https://www.djangoproject.com/)
* **API:** [Django REST Framework (DRF)](https://www.django-rest-framework.org/) & [drf-spectacular](https://drf-spectacular.readthedocs.io/)
* **Package Manager:** [Poetry 2.3+](https://python-poetry.org/)
* **Admin UI:** [Django Unfold](https://github.com/unfoldadmin/django-unfold) (Modern Tailwind-based Admin)
* **Async Tasks:** Celery + Celery Beat
* **Testing:** Pytest

### Frontend (React)
* **Build Tool:** [Vite](https://vitejs.dev/)
* **Library:** [React](https://react.dev/)
* **Styling:** [Tailwind CSS v4](https://tailwindcss.com/) (Native CSS engine, no `tailwind.config.js` required)

---

## 📁 Project Structure

```text
.
├── backend/                # Django Project Root
│   ├── core/               # Main Application Domain
│   │   ├── admin/          # Modular Admin (User, dashboard, celery)
│   │   ├── api/            # DRF Serializers & ViewSets
│   │   ├── migrations/     # Database Migrations
│   │   ├── models/         # Modular Models (Base, User)
│   │   ├── settings/       # Split Settings (base.py, development.py, production.py)
│   │   ├── static/         # Global assets
│   │   └── templates/      # Base HTML & Vite layouts
│   ├── staticfiles/        # Additional static assets
│   └── manage.py           # Dynamic manage.py (auto-detects environment)
├── db/                     # SQLite Database directory (auto-generated)
├── docs/                   # Documentation directory
│   └── README.md           # The main project documentation
├── frontend/               # Vite + React Project
│   ├── src/
│   │   ├── index.css       # Tailwind v4 @import
│   │   └── App.jsx
│   └── vite.config.js      # Vite & Tailwind plugin config
├── scripts/                # DevOps & Cleanup Utilities
│   └── customize.py        # Project initialization script
├── tests/                  # Pytest Suite
├── .env.example            # Environment variables template
├── pyproject.toml          # Poetry Configuration & Poe Tasks
└── LICENSE                 # Open-source license
```

---

## 📋 Prerequisites
Before you begin, ensure you have the following installed on your system:
* **Python** (>= 3.12)
* **Poetry** (>= 2.3.x)
* **Node.js** (>= 20.x) and **npm**
* **Git**

---

## 🚀 Getting Started

### Step 1: Clone & Customize
Clone the boilerplate repository into your new project directory. Do not run any install commands yet.

```bash
git clone [https://github.com/git-evinci/django-react-boilerplate.git](https://github.com/git-evinci/django-react-boilerplate.git) my-new-project
cd my-new-project
```

Run the initialization script using your system Python. This script automatically rebrands `pyproject.toml`, the `LICENSE`, and generates a secure `.env` file:
```bash
python scripts/customize.py
```
*(Follow the interactive prompts to set your Project Slug, Author Name, etc.)*

### Step 2: Backend & Environment Setup
Install the Python dependencies using Poetry:
```bash
poetry install
```

The initialization script created a `.env` file for you based on `.env.example`. Ensure it looks like this:
```env
DJANGO_ENV=development
PYTHONPATH=./backend
DEBUG=True
SECRET_KEY=<your_auto_generated_50_char_key>
ALLOWED_HOSTS=localhost,127.0.0.1
UNFOLD_STUDIO=0
```

### Step 3: Database & Migrations
Because Git does not track empty folders, you must manually initialize your `migrations` directory before Django can detect your modular models.

1. **Ensure the migrations module exists:**
   ```bash
   mkdir -p backend/core/migrations
   touch backend/core/migrations/__init__.py
   ```

2. **Generate the migration files:**
   ```bash
   poetry run python backend/manage.py makemigrations core
   ```

3. **Apply migrations to the SQLite database:**
   *(The `db/` folder will be auto-created by settings if it doesn't exist)*
   ```bash
   poetry run python backend/manage.py migrate
   ```

4. **Create a Superuser for the Unfold Admin panel:**
   ```bash
   poetry run python backend/manage.py createsuperuser
   ```

### Step 4: Frontend (React + Tailwind v4)
Our frontend uses the new Tailwind CSS v4, which operates as a lightning-fast Vite plugin rather than a PostCSS wrapper.

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node dependencies:**
   ```bash
   npm install
   ```

3. **Verify Environment Configuration:**
   Ensure your frontend `.env` (or `.env.local`) points to the Django API:
   ```env
   VITE_API_URL=[http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)
   ```

---

## 💻 Development

### Running the Servers
You will need two terminal windows to run both the frontend and backend simultaneously.

**Terminal 1: Django Backend**
From the root directory, run our custom Poe task:
```bash
poe dev
```

**Terminal 2: Vite Frontend**
From the `frontend` directory:
```bash
npm run dev
```

### Accessing the Application
* **React App:** `http://localhost:5173/`
* **Django Unfold Admin:** `http://127.0.0.1:8000/admin/`
* **API Endpoints:** `http://127.0.0.1:8000/api/`

### API Documentation (Swagger/Redoc)
The boilerplate includes `drf-spectacular` for OpenAPI 3.0 schema generation.
* **Interactive Swagger UI:** `http://127.0.0.1:8000/api/docs/`
* **Redoc UI:** `http://127.0.0.1:8000/api/redoc/`

**Export Schema for Frontend (TypeScript Generation):**
```bash
poe schema
```
*(This generates a `schema.yml` file in the root directory).*

---

## ⚠️ Troubleshooting & Gotchas

#### 1. `OperationalError: no such table: core_userprofile` (During createsuperuser)
* **Cause:** You ran `createsuperuser` before Django detected your `UserProfile` model in the `core` app.
* **Fix:** Ensure `backend/core/migrations/__init__.py` exists. Run `makemigrations core`, then `migrate`, and finally try `createsuperuser` again.

#### 2. `django_vite.W001: Cannot read Vite manifest file`
* **Cause:** Django is looking for a production `manifest.json` file in `frontend/dist/`.
* **Fix:** Ignore this during development. It is normal. To permanently clear the warning, run a production build once: `cd frontend && npm run build`.

#### 3. `unable to open database file`
* **Cause:** SQLite cannot find the `db/` parent folder.
* **Fix:** If the `BASE_DIR.parent / "db".mkdir(...)` fallback in `settings.py` fails, manually run `mkdir db` in the project root.

#### 4. Missing Static Folders Warning (`staticfiles.W004`)
* **Cause:** Git ignores empty directories, so `backend/static/` might be missing.
* **Fix:** Manually create them: `mkdir -p backend/static backend/staticfiles`.

#### 5. Blank Swagger UI Page
* **Cause:** You are using the "SIDECAR" setting but haven't installed the sidecar package.
* **Fix:** Either run `poetry add drf-spectacular-sidecar` **OR** remove `SWAGGER_UI_DIST: 'SIDECAR'` from your `SPECTACULAR_SETTINGS` in `base.py` to fall back to the CDN.
