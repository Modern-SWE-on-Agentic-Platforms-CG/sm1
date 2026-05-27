def test_login_valid(client, db):
    """Valid credentials return 200 and a token."""
    from app.core.security import hash_password
    from app.models.employee import EmployeeMaster, EmployeeRoleDetails
    from app.models.master_data import RoleMaster

    role = RoleMaster(role_name="Recruiter_test")
    db.add(role)
    db.flush()
    emp = EmployeeMaster(
        emp_name="Recruiter",
        email_id="recruiter@test.local",
        password_hash=hash_password("Pass@123"),
        bu="Digital",
    )
    db.add(emp)
    db.flush()
    db.add(EmployeeRoleDetails(emp_id=emp.emp_id, role_id=role.id))
    db.commit()

    resp = client.post("/api/v1/auth/login", json={"email": "recruiter@test.local", "password": "Pass@123"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "success"
    assert "access_token" in body["data"]


def test_login_invalid(client):
    """Invalid password returns 401."""
    resp = client.post("/api/v1/auth/login", json={"email": "nobody@test.local", "password": "wrong"})
    assert resp.status_code == 401
    assert resp.json()["status"] == "error"


def test_me_with_token(client, admin_token):
    """GET /me with valid token returns employee data."""
    resp = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {admin_token}"})
    assert resp.status_code == 200
    assert resp.json()["data"]["email_id"] == "admin@test.local"
