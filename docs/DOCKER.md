# 🐳 Docker Cheat Sheet & Environment Guide

This guide provides a comprehensive reference for managing the Django-React stack using Docker Compose. The environment is engineered for **Full Parity**, sharing the same SQLite database and environment variables with your local standalone development.

---

## 📑 Table of Contents
1. [Basic Orchestration](#-basic-orchestration)
2. [Independent Service Management](#-independent-service-management)
3. [Executing Management Tasks](#-executing-management-tasks)
4. [Volume & Data Management](#-volume--data-management)
5. [Troubleshooting & Gotchas](#-troubleshooting--gotchas)

---

## 🏗 Basic Orchestration

Use these commands to manage the lifecycle of the entire application stack.

### Start the Stack
```bash
# Standard start (logs visible)
docker compose -f docker/docker-compose.yml up

# Detached mode (runs in background)
docker compose -f docker/docker-compose.yml up -d
```

### Build and Rebuild
*Run this after modifying Dockerfiles, `pyproject.toml`, or `package.json`.*
```bash
docker compose -f docker/docker-compose.yml up --build
```

### Stop and Cleanup
```bash
# Stop containers but keep them created
docker compose -f docker/docker-compose.yml stop

# Stop and remove containers, networks, and images
docker compose -f docker/docker-compose.yml down
```

---

## 🚦 Independent Service Management

You can target specific services (`backend` or `frontend`) to save system resources or focus on one layer.

### Single Service Startup
```bash
# Start only the Django API
docker compose -f docker/docker-compose.yml up backend

# Start only the Vite/React UI
docker compose -f docker/docker-compose.yml up frontend
```

### Hybrid Startup
Start the backend in the background while keeping the frontend logs active:
```bash
docker compose -f docker/docker-compose.yml up -d backend
docker compose -f docker/docker-compose.yml up frontend
```

---

## 🛠 Executing Management Tasks

Run these commands while the containers are **active** to perform administrative actions inside the virtualized environment.

### 🐍 Backend (Django)
| Task | Command |
| :--- | :--- |
| **Migrations** | `docker exec -it evinci_django python backend/manage.py makemigrations` |
| **Apply DB** | `docker exec -it evinci_django python backend/manage.py migrate` |
| **Superuser** | `docker exec -it evinci_django python backend/manage.py createsuperuser` |
| **Django Shell** | `docker exec -it evinci_django python backend/manage.py shell` |

### ⚛️ Frontend (React/Node)
| Task | Command |
| :--- | :--- |
| **Install Pkg** | `docker exec -it evinci_react npm install <package-name>` |
| **Check Version**| `docker exec -it evinci_react node -v` |

---

## 📂 Volume & Data Management

### 🗄 Shared SQLite Database
The database is synced via a host volume. This allows you to switch between Docker and Standalone development without losing data.
* **Host Location:** `./db/db.sqlite3`
* **Container Path:** `/app/db/db.sqlite3`

### 📦 Node Modules Isolation
To avoid conflicts between Linux (Docker) and your Host OS, `node_modules` are managed via an anonymous volume. Local changes to `package.json` require an `up --build` to sync.

---

## ⚠️ Troubleshooting & Gotchas

### 1. Permission Denied (db.sqlite3)
If Docker creates the DB file, it may be owned by `root`.
**Fix:** 
```bash
sudo chown -R $USER:$USER db/
```

### 2. DisallowedHost Error
If the browser shows an `Invalid HTTP_HOST` error for `0.0.0.0`.
**Fix:** Ensure your `.env` contains:
```env
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

### 3. Database is Locked
Occurs if you try to run migrations locally while the Docker container is still running.
**Fix:** Stop the `evinci_django` container before running standalone management commands.