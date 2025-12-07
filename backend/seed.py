"""
Seed script to populate the database with initial team members.
Run this script to set up the database with test users.

Usage: python seed.py
"""
from app.database import SessionLocal, engine, Base
from app.models import User
from app.auth import hash_password
from app.schemas import StatusEnum

# Create all tables
Base.metadata.create_all(bind=engine)

# Team members to seed
TEAM_MEMBERS = [
    {
        "username": "samc",
        "password": "password123",
        "full_name": "Sam Cooke",
        "status": StatusEnum.WORKING,
    },
    {
        "username": "afranklin",
        "password": "password123",
        "full_name": "Aretha Franklin",
        "status": StatusEnum.WORKING_REMOTELY,
    },
    {
        "username": "kingluther",
        "password": "password123",
        "full_name": "Luther Vandross",
        "status": StatusEnum.ON_VACATION,
    },
    {
        "username": "gknight",
        "password": "password123",
        "full_name": "Gladys Knight",
        "status": StatusEnum.BUSINESS_TRIP,
    },
    {
        "username": "otis",
        "password": "password123",
        "full_name": "Otis Redding",
        "status": StatusEnum.WORKING,
    },
]


def seed_database():
    """Seed the database with team members."""
    db = SessionLocal()
    
    try:
        # Check if database already has users
        existing_count = db.query(User).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} user(s). Skipping seed.")
            print("To re-seed, delete team_presence.db and run again.")
            return
        
        # Create users
        for member in TEAM_MEMBERS:
            user = User(
                username=member["username"],
                password_hash=hash_password(member["password"]),
                full_name=member["full_name"],
                status=member["status"].value,
            )
            db.add(user)
        
        db.commit()
        
        print("✅ Database seeded successfully!")
        print("\n📋 Team Members Created:")
        print("-" * 50)
        for member in TEAM_MEMBERS:
            print(f"  Username: {member['username']}")
            print(f"  Password: {member['password']}")
            print(f"  Name: {member['full_name']}")
            print("-" * 50)
        
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()

