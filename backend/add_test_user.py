"""Quick script to add a test user for testing."""
from app.database import SessionLocal, engine, Base
from app.models import User
from app.auth import hash_password

# Create tables
Base.metadata.create_all(bind=engine)

# Create session
db = SessionLocal()

# Check if test user exists
existing = db.query(User).filter(User.username == "test").first()

if existing:
    print("Test user already exists!")
else:
    # Create test user
    user = User(
        username="test",
        password_hash=hash_password("test123"),
        full_name="Test User",
        status=0  # Working
    )
    db.add(user)
    db.commit()
    print("Created test user:")
    print("  Username: test")
    print("  Password: test123")

db.close()

