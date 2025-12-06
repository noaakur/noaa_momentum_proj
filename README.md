# Team Presence Dashboard

Momentum's internal **Team Presence Dashboard** — a lightweight system our distributed team will use to understand who's available, who's offline, and how the team is operating in real time.

## 🎯 Project Definition

a full-stack system with secure authentication, a clean API, and a basic UI that allows users to:

- **Log in** with username and password
- **Update their availability status** (Working, Working Remotely, On Vacation, Business Trip)
- **View teammates and their statuses**
- **Filter by status**

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python + FastAPI |
| **Database** | SQLite + SQLAlchemy |
| **Authentication** | JWT (python-jose + bcrypt) |
| **Frontend** | React (Vite) |
| **Containerization** | Docker + docker-compose |


## 📁 Project Structure

```
├── backend/          # FastAPI backend
├── frontend/         # React frontend
├── docker-compose.yml
└── README.md
```

## 📋 Implementation Order

1. **Backend Setup** - FastAPI app structure, config, database connection
2. **Models & Schemas** - User model, Pydantic schemas
3. **Auth** - Password hashing, JWT generation/validation, login endpoint
4. **Team Routes** - GET /team, PATCH /me/status with auth protection
5. **Seed Script** - Create the 4 users
6. **Frontend** - Login page, Dashboard with status update & filtering
7. **Docker** - Dockerfiles + docker-compose
8. **README** - Add clear run instructions to the file
