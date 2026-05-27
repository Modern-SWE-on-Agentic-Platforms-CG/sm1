"""
Backend test configuration.
Uses a separate PostgreSQL test schema to avoid polluting the main DB.
"""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Override DB for tests
TEST_DB_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://postgres:@localhost:5432/smarthiremain001_test",
)

os.environ["DB_NAME"] = "smarthiremain001_test"

from app.core.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402

engine = create_engine(TEST_DB_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def create_tables():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def admin_token(client, db):
    """Seed admin and return JWT token."""
    from app.core.security import hash_password
    from app.models.employee import EmployeeMaster, EmployeeRoleDetails
    from app.models.master_data import RoleMaster

    role = db.query(RoleMaster).filter(RoleMaster.role_name == "Admin").first()
    if not role:
        role = RoleMaster(role_name="Admin")
        db.add(role)
        db.flush()

    admin = db.query(EmployeeMaster).filter(EmployeeMaster.email_id == "admin@test.local").first()
    if not admin:
        admin = EmployeeMaster(
            emp_name="Test Admin",
            email_id="admin@test.local",
            password_hash=hash_password("Test@123"),
            bu="Corporate",
        )
        db.add(admin)
        db.flush()
        db.add(EmployeeRoleDetails(emp_id=admin.emp_id, role_id=role.id))
    db.commit()

    resp = client.post("/api/v1/auth/login", json={"email": "admin@test.local", "password": "Test@123"})
    return resp.json()["data"]["access_token"]
