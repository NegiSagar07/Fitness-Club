# Fitness Club API (Yoga Class Booking System)

A **FastAPI** backend for a **fitness club / yoga studio booking platform**. It lets you manage **users**, **instructors**, **yoga classes**, **schedules**, **sessions**, and **bookings**.

> **Status:** MVP / learning project. The repository also includes a `BLUEPRINT.md` describing the planned roadmap and data model.

---

## Table of Contents

- [Project Overview](#project-overview)
- [What This Project Does (Features)](#what-this-project-does-features)
- [Tech Stack](#tech-stack)
- [Repository Structure](#repository-structure)
- [High-Level Architecture](#high-level-architecture)
- [Database Design (Entities)](#database-design-entities)
- [API Modules & Routes](#api-modules--routes)
- [Local Setup](#local-setup)
- [Environment Variables](#environment-variables)
- [Run the App](#run-the-app)
- [Using the API (Examples)](#using-the-api-examples)
- [Common Troubleshooting](#common-troubleshooting)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview

This project is a backend API for a fitness club that offers yoga classes. The API supports the full flow:

1. **Create users** (members) and **instructors**.
2. **Create yoga classes** (the kind of class, e.g., “Hatha Yoga”).
3. **Create schedules** (recurring weekly availability for an instructor + class).
4. **Create sessions** (specific time-based classes that can be booked).
5. **Book sessions** and **cancel bookings**.

The goal is to keep the codebase simple, modular, and easy to extend.

---

## What This Project Does (Features)

### Core resources

- **Users**: register and store member information.
- **Instructors**: store instructors who can run sessions.
- **Yoga Classes**: define class types (name, description).
- **Schedules**: weekly recurring schedule (day of week + time range) with max participants & fee.
- **Sessions**: actual scheduled occurrences with start/end datetime.
- **Bookings**: a user reserves a spot in a session.

### Typical workflows

- Admin/staff creates a yoga class, an instructor, then creates schedules/sessions.
- A user lists sessions and books one.
- The system tracks the booking status and participant counts.

---

## Tech Stack

- **Python** (backend language)
- **FastAPI** (web framework)
- **Uvicorn** (ASGI server)
- **SQLAlchemy** (ORM)
- **asyncpg** (PostgreSQL async driver)
- **Pydantic** (request/response validation)

Dependencies are pinned in [`requirements.txt`](requirements.txt).

---

## Repository Structure

```text
.
├── app/
│   ├── main.py            # FastAPI app creation + router registration
│   ├── database.py        # DB engine/session setup + init_db() table creation
│   ├── models.py          # SQLAlchemy models (tables)
│   ├── schema.py          # Pydantic schemas (DTOs)
│   ├── core/              # shared utilities / settings (project-specific)
│   ├── crud/              # database operations (create/read/update/delete)
│   └── routes/            # API endpoints grouped by resource
│       ├── user.py
│       ├── instructor.py
│       ├── yoga_class.py
│       ├── yoga_schedule.py
│       ├── yoga_session.py
│       └── booking.py
├── BLUEPRINT.md           # MVP roadmap + suggested schema & services
├── requirements.txt       # Python dependencies
└── .gitignore
```

---

## High-Level Architecture

This project follows a common FastAPI layout:

- **Routes (`app/routes/`)**: define HTTP endpoints and validate input/output.
- **Schemas (`app/schema.py`)**: Pydantic models used by routes.
- **Models (`app/models.py`)**: SQLAlchemy models that map to DB tables.
- **CRUD (`app/crud/`)**: functions that implement database interactions.
- **Database (`app/database.py`)**: creates the DB connection and initializes tables.

### App startup lifecycle

In [`app/main.py`](app/main.py), a **FastAPI lifespan** hook calls `init_db()` on startup to ensure tables exist.

---

## Database Design (Entities)

The blueprint defines the main entities (and this is mirrored in the codebase models):

- **user**: id, name, email, password
- **instructor**: id, name, email, password
- **yoga_class**: id, name, description
- **session**: yoga_class_id, instructor_id, start_time, end_time, max_participants, current_participants, fee
- **schedule**: yoga_class_id, instructor_id, day_of_week, start_time, end_time, fee, max_participants
- **booking**: user_id, session_id, booking_time, status

> Note: passwords should be stored as **hashed** values (never plaintext). If your current implementation stores plaintext, treat it as a learning-only implementation and update it.

---

## API Modules & Routes

The app registers these routers (see `app/main.py`):

- `app/routes/user.py`
- `app/routes/instructor.py`
- `app/routes/yoga_class.py`
- `app/routes/yoga_session.py`
- `app/routes/yoga_schedule.py`
- `app/routes/booking.py`

Once the server is running, you can explore the API using:

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

---

## Local Setup

### 1) Clone the repository

```bash
git clone https://github.com/NegiSagar07/Fitness-Club.git
cd Fitness-Club
```

### 2) Create & activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

This project uses a database connection (commonly PostgreSQL, because `asyncpg` is installed).

Create a `.env` file in the project root (recommended):

```env
# Example (adjust for your machine)
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/fitness_club
```

If your code expects a different variable name, update the `.env` accordingly.

---

## Run the App

From the repository root:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

- `http://127.0.0.1:8000/`

On startup, `init_db()` is executed to initialize the database tables.

---

## Using the API (Examples)

> These are example calls. The exact request/response shapes depend on the schemas in `app/schema.py`.

### Health / root

```bash
curl http://127.0.0.1:8000/
```

### Create a user (example)

```bash
curl -X POST http://127.0.0.1:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Sagar","email":"sagar@example.com","password":"secret"}'
```

### Create an instructor (example)

```bash
curl -X POST http://127.0.0.1:8000/instructors/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Coach","email":"coach@example.com","password":"secret"}'
```

### Create a yoga class (example)

```bash
curl -X POST http://127.0.0.1:8000/yoga-classes/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Hatha Yoga","description":"Beginner friendly"}'
```

---

## Common Troubleshooting

### `ModuleNotFoundError: No module named 'app'`

Run commands from the **repository root** so Python can find the `app/` package.

### Database connection errors

- Ensure PostgreSQL is running.
- Verify `DATABASE_URL` is correct.
- Ensure the database exists (create it if needed).

### Tables not created

`init_db()` runs during the app startup lifespan; if you changed DB settings, restart the server.

---

## Roadmap

Planned work is captured in [`BLUEPRINT.md`](BLUEPRINT.md):

- Phase 1: user/instructor creation + booking
- Phase 2: database schema
- Phase 3: CRUD/services layers

---

## Contributing

Contributions are welcome.

1. Fork the repo
2. Create a feature branch
3. Commit your changes
4. Open a PR

Please keep changes small and focused, and update the README if behavior changes.

---

## License

No license file is currently included. If you want this to be open-source, add a `LICENSE` (MIT is common for learning projects).