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



