# Team Presence Dashboard

Momentum's internal **Team Presence Dashboard** — a lightweight system for distributed teams to understand who's available, who's offline, and how the team is operating in real time.

---

## 🎯 Features

- **Login** with username and password (JWT authentication)
- **Update your availability status** (Working, Working Remotely, On Vacation, Business Trip)
- **View all team members** with their current status and last update time
- **Filter by status** (supports multi-select filtering)

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.11 + FastAPI |
| **Database** | SQLite + SQLAlchemy |
| **Authentication** | JWT (python-jose + bcrypt) |
| **Frontend** | React 18 + Vite |
| **Containerization** | Docker + Docker Compose |

---

## 🚀 Quick Start (Recommended)

### Prerequisites

- **Docker** and **Docker Compose** installed on your machine
  - [Install Docker](https://docs.docker.com/get-docker/)
  - Docker Compose is included with Docker Desktop

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd noaa_momentum_proj
```

### Step 2: Start the Application

Run the following command from the project root directory:

```bash
docker compose up --build
```

This command will:
1. Build the backend Docker image (Python/FastAPI)
2. Build the frontend Docker image (React/Nginx)
3. Start both containers
4. **Automatically seed the database** with 5 test users

Wait for the build to complete. You'll see logs from both services. When you see:
```
momentum-backend  | INFO:     Uvicorn running on http://0.0.0.0:8000
```

The application is ready!

### Step 3: Access the Application

Open your browser and navigate to:

| What | URL | Note |
|------|-----|------|
| **🖥️ Frontend (Main UI)** | **http://localhost:3000** | Docker only |
| **📡 Backend API** | http://localhost:8000 | |
| **📚 API Documentation** | http://localhost:8000/docs | |

### Step 4: Login

Use any of the following test credentials:

| Username | Password | Initial Status |
|----------|----------|----------------|
| `samc` | `password123` | Working |
| `afranklin` | `password123` | Working Remotely |
| `kingluther` | `password123` | On Vacation |
| `gknight` | `password123` | Business Trip |
| `otis` | `password123` | Working |

### Step 5: Stop the Application

Press `Ctrl+C` in the terminal, or run:

```bash
docker compose down
```

To also remove the database volume (reset all data):

```bash
docker compose down -v
```

---

## 🗄️ Database Setup

### Automatic Seeding (Docker)

When running with Docker, the database is **automatically seeded** on first startup. The seed script creates:
- 5 team members with usernames, hashed passwords, and initial statuses
- A SQLite database file stored in a Docker volume for persistence

### Manual Seeding (Local Development)

If running locally without Docker, seed the database manually:

```bash
cd backend
python seed.py
```

Expected output:
```
✅ Database seeded successfully!

📋 Team Members Created:
--------------------------------------------------
  Username: samc
  Password: password123
  Name: Sam Cooke
--------------------------------------------------
  ... (4 more users)
```

### Re-seeding the Database

To reset and re-seed the database:

**Docker:**
```bash
docker compose down -v    # Remove volume
docker compose up --build # Rebuild and restart
```

**Local:**
```bash
cd backend
rm team_presence.db       # Delete existing database
python seed.py            # Re-run seed script
```

### Adding New Users

To add individual users to the database, use the `add_test_user.py` script as a template:

```bash
cd backend
python add_test_user.py
```

This creates a user with username `test` and password `test123`.

**To add a custom user**, edit `add_test_user.py` or create a similar script.

---

## 🔌 Port Reference

| Service | Docker | Local Development |
|---------|--------|-------------------|
| **Frontend** | http://localhost:3000 | http://localhost:5173 |
| **Backend** | http://localhost:8000 | http://localhost:8000 |

---

## 💻 Local Development (Without Docker)

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Seed the database (first time only)
python seed.py

# Start the development server
uvicorn app.main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173` (Vite dev server)

> **Note:** In local development, the frontend runs on port **5173** (Vite).  
> When running with Docker, the frontend runs on port **3000** (Nginx).

### Running Tests

```bash
cd backend

# Make sure the backend server is running in another terminal
python tests.py
```

Expected output:
```
============================================================
Running Team Presence Dashboard API Tests
============================================================

✅ test_health_check passed
✅ test_login_success passed
... (16 total tests)

============================================================
Results: 16 passed, 0 failed
============================================================
```

---

## 📁 Project Structure

```
noaa_momentum_proj/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── routes/
│   │   │   ├── auth.py         # POST /login endpoint
│   │   │   └── team.py         # GET /team, PATCH /me/status
│   │   ├── auth.py             # JWT & password utilities
│   │   ├── config.py           # Application settings
│   │   ├── database.py         # SQLAlchemy setup
│   │   ├── models.py           # User database model
│   │   ├── schemas.py          # Pydantic request/response schemas
│   │   └── main.py             # FastAPI app initialization
│   ├── seed.py                 # Database seed script
│   ├── tests.py                # API test suite
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Login.jsx       # Login page component
│   │   │   └── Dashboard.jsx   # Main dashboard component
│   │   ├── context/
│   │   │   └── AuthContext.jsx # Authentication state management
│   │   ├── api.js              # API service functions
│   │   ├── App.jsx             # Root component
│   │   └── App.css             # Styles
│   ├── public/
│   │   ├── small_logo.svg      # Favicon
│   │   └── big_logo.svg        # Logo
│   ├── nginx.conf              # Nginx configuration for production
│   └── Dockerfile
├── docker-compose.yml          # Docker orchestration
└── README.md
```

---

## 📡 API Reference

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/login` | Authenticate and get JWT token | ❌ No |

**Request Body:**
```json
{
  "username": "samc",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### Team Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/team` | Get all team members | ✅ Yes |
| `GET` | `/team?status=0` | Filter by single status | ✅ Yes |
| `GET` | `/team?status=0&status=1` | Filter by multiple statuses | ✅ Yes |
| `PATCH` | `/me/status` | Update your status | ✅ Yes |

**Authorization Header:**
```
Authorization: Bearer <access_token>
```

**Status Values:**

| Value | Label |
|-------|-------|
| `0` | Working |
| `1` | Working Remotely |
| `2` | On Vacation |
| `3` | Business Trip |

**PATCH /me/status Request:**
```json
{
  "status": 1
}
```

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Returns `{"status": "healthy"}` |

---

## 🔐 Authentication Flow

1. User submits username and password to `POST /login`
2. Server validates credentials against hashed passwords in database
3. On success, server returns a JWT token (valid for 30 minutes)
4. Client stores the token and includes it in subsequent requests:
   ```
   Authorization: Bearer <token>
   ```
5. Protected endpoints validate the token before processing requests

---

## 📝 Design Decisions

| Decision | Rationale |
|----------|-----------|
| **SQLite** | Lightweight, no separate DB service needed. Perfect for this scale and easy local development. |
| **JWT Authentication** | Stateless, scalable, industry standard. No server-side session storage required. |
| **Pydantic Schemas** | Type-safe request/response validation with automatic OpenAPI documentation. |
| **React Context** | Simple auth state management without the overhead of Redux for this small app. |
| **Multi-stage Docker builds** | Smaller production images (frontend goes from ~1GB Node to ~40MB Nginx). |
| **Status as integer** | Efficient storage and filtering, with label mapping for display. |
| **bcrypt** | Industry-standard password hashing with automatic salting. |

---

## 🐛 Troubleshooting

### Port already in use

```bash
# Check what's using port 8000 or 3000
lsof -i :8000
lsof -i :3000

# Kill the process or stop existing containers
docker compose down
```

### Database not seeding

```bash
# Remove the volume and rebuild
docker compose down -v
docker compose up --build
```

### Changes not reflecting

```bash
# Rebuild containers after code changes
docker compose up --build
```

---

## 📄 License

This project was created as a home exercise for Momentum.
