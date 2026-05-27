"""
Idempotent seed script — safe to run multiple times.
Usage (from repo root): python backend/seed_data.py
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from app.core.database import SessionLocal, engine, Base
from app.core.security import hash_password
from app.models.master_data import RoleMaster, TowerMaster, TechnologyMaster, SourceMaster, VendorMaster
from app.models.employee import EmployeeMaster, EmployeeRoleDetails
import app.models.interview  # noqa: F401 — needed for ORM relationship resolution
from app.models.candidate import StatusIntermediateMapping
from app.models.referral import ReferralTechnologyMaster, ReferralNoticePeriodMaster, ReferralLocationMaster

ROLES = [
    "Interviewer", "Recruiter", "PMO", "PracticeLead", "Lead",
    "TowerLead", "SLBULead", "NALead", "RecruiterLead", "BUAdmin",
    "PracticeAdmin", "Admin", "ReferralSPOC", "ReferralUser",
]

TOWERS = ["Java", "Python", "SAP", ".NET", "QA", "DevOps", "Data & AI", "Cloud"]

TECHNOLOGIES = [
    {"tech_name": "Java", "skill_group": "Backend", "tower_name": "Java"},
    {"tech_name": "Spring Boot", "skill_group": "Backend", "tower_name": "Java"},
    {"tech_name": "Python", "skill_group": "Backend", "tower_name": "Python"},
    {"tech_name": "FastAPI", "skill_group": "Backend", "tower_name": "Python"},
    {"tech_name": "Django", "skill_group": "Backend", "tower_name": "Python"},
    {"tech_name": "React", "skill_group": "Frontend", "tower_name": "Java"},
    {"tech_name": "Angular", "skill_group": "Frontend", "tower_name": ".NET"},
    {"tech_name": "SAP ABAP", "skill_group": "SAP", "tower_name": "SAP"},
    {"tech_name": "SAP SD", "skill_group": "SAP", "tower_name": "SAP"},
    {"tech_name": "C#", "skill_group": "Backend", "tower_name": ".NET"},
    {"tech_name": "Selenium", "skill_group": "QA", "tower_name": "QA"},
    {"tech_name": "Docker", "skill_group": "DevOps", "tower_name": "DevOps"},
    {"tech_name": "Kubernetes", "skill_group": "DevOps", "tower_name": "DevOps"},
    {"tech_name": "AWS", "skill_group": "Cloud", "tower_name": "Cloud"},
    {"tech_name": "Azure", "skill_group": "Cloud", "tower_name": "Cloud"},
    {"tech_name": "Machine Learning", "skill_group": "Data & AI", "tower_name": "Data & AI"},
    {"tech_name": "Power BI", "skill_group": "Data & AI", "tower_name": "Data & AI"},
]

STATUS_TRANSITIONS = [
    ("Profile Received", "L1 Scheduled"),
    ("L1 Scheduled", "L1 Selected"),
    ("L1 Scheduled", "L1 Rejected"),
    ("L1 Scheduled", "L1 Hold"),
    ("L1 Scheduled", "L1 Completed"),
    ("L1 Scheduled", "L1 No Show"),
    ("L1 Scheduled", "L1 Cancelled"),
    ("L1 Selected", "L2 Scheduled"),
    ("L2 Scheduled", "L2 Selected"),
    ("L2 Scheduled", "L2 Rejected"),
    ("L2 Scheduled", "L2 Hold"),
    ("L2 Scheduled", "L2 Completed"),
    ("L2 Scheduled", "L2 No Show"),
    ("L2 Selected", "Offered"),
    ("L2 Selected", "L3 Scheduled"),
    ("L3 Scheduled", "Offered"),
    ("Offered", "Offer Approved"),
    ("Offer Approved", "Offer Released"),
    ("Offer Released", "Offer Accepted"),
    ("Offer Released", "Offer Declined"),
    ("Offer Accepted", "Joined"),
    ("Offer Accepted", "Not Joined"),
]

SOURCES = ["Naukri", "LinkedIn", "Referral", "Walk-in", "Job Portal", "Campus", "Internal", "Vendor"]
VENDORS = ["ABC Staffing", "XYZ Consultants", "Tech Recruit Pvt Ltd"]

REFERRAL_TECHNOLOGIES = ["Java", "Python", "SAP", ".NET", "React", "Angular", "DevOps", "QA", "Data & AI", "Cloud"]
REFERRAL_NOTICE_PERIODS = ["Immediate", "15 days", "30 days", "45 days", "60 days", "90 days"]
REFERRAL_LOCATIONS = ["Bangalore", "Mumbai", "Delhi", "Hyderabad", "Chennai", "Pune", "Remote"]


def seed():
    db = SessionLocal()
    try:
        # Roles
        for role_name in ROLES:
            existing = db.query(RoleMaster).filter(RoleMaster.role_name == role_name).first()
            if not existing:
                db.add(RoleMaster(role_name=role_name))
        db.commit()
        print(f"✓ Roles seeded ({len(ROLES)})")

        # Towers
        tower_map: dict[str, int] = {}
        for tower_name in TOWERS:
            existing = db.query(TowerMaster).filter(TowerMaster.tower_name == tower_name).first()
            if not existing:
                t = TowerMaster(tower_name=tower_name)
                db.add(t)
                db.flush()
                tower_map[tower_name] = t.id
            else:
                tower_map[tower_name] = existing.id
        db.commit()
        print(f"✓ Towers seeded ({len(TOWERS)})")

        # Technologies
        for tech in TECHNOLOGIES:
            tower_id = tower_map.get(tech["tower_name"])
            existing = (
                db.query(TechnologyMaster)
                .filter(
                    TechnologyMaster.tech_name == tech["tech_name"],
                    TechnologyMaster.tower_id == tower_id,
                )
                .first()
            )
            if not existing:
                db.add(TechnologyMaster(
                    tech_name=tech["tech_name"],
                    skill_group=tech["skill_group"],
                    tower_id=tower_id,
                ))
        db.commit()
        print(f"✓ Technologies seeded ({len(TECHNOLOGIES)})")

        # Status transitions
        for from_s, to_s in STATUS_TRANSITIONS:
            existing = (
                db.query(StatusIntermediateMapping)
                .filter(
                    StatusIntermediateMapping.from_status == from_s,
                    StatusIntermediateMapping.to_status == to_s,
                )
                .first()
            )
            if not existing:
                db.add(StatusIntermediateMapping(from_status=from_s, to_status=to_s))
        db.commit()
        print(f"✓ Status transitions seeded ({len(STATUS_TRANSITIONS)})")

        # Admin user
        admin_email = "admin@smartrecruit.dev"
        existing_admin = db.query(EmployeeMaster).filter(EmployeeMaster.email_id == admin_email).first()
        if not existing_admin:
            admin = EmployeeMaster(
                emp_name="System Admin",
                email_id=admin_email,
                password_hash=hash_password("Admin@123"),
                bu="Corporate",
                organisation="Smart Recruit",
                is_active=True,
            )
            db.add(admin)
            db.flush()
            admin_role = db.query(RoleMaster).filter(RoleMaster.role_name == "Admin").first()
            if admin_role:
                db.add(EmployeeRoleDetails(emp_id=admin.emp_id, role_id=admin_role.id))
            db.commit()
            print("✓ Admin user seeded: admin@smartrecruit.dev / Admin@123")
        else:
            print("✓ Admin user already exists")

        # Sources
        for source_name in SOURCES:
            if not db.query(SourceMaster).filter(SourceMaster.source_name == source_name).first():
                db.add(SourceMaster(source_name=source_name))
        db.commit()
        print(f"✓ Sources seeded ({len(SOURCES)})")

        # Vendors
        for vendor_name in VENDORS:
            if not db.query(VendorMaster).filter(VendorMaster.vendor_name == vendor_name).first():
                db.add(VendorMaster(vendor_name=vendor_name))
        db.commit()
        print(f"✓ Vendors seeded ({len(VENDORS)})")

        # Referral master data
        for tech_name in REFERRAL_TECHNOLOGIES:
            if not db.query(ReferralTechnologyMaster).filter(ReferralTechnologyMaster.tech_name == tech_name).first():
                db.add(ReferralTechnologyMaster(tech_name=tech_name))
        db.commit()
        print(f"✓ Referral technologies seeded ({len(REFERRAL_TECHNOLOGIES)})")

        for np in REFERRAL_NOTICE_PERIODS:
            if not db.query(ReferralNoticePeriodMaster).filter(ReferralNoticePeriodMaster.period_label == np).first():
                db.add(ReferralNoticePeriodMaster(period_label=np))
        db.commit()
        print(f"✓ Referral notice periods seeded ({len(REFERRAL_NOTICE_PERIODS)})")

        for location_name in REFERRAL_LOCATIONS:
            if not db.query(ReferralLocationMaster).filter(ReferralLocationMaster.location_name == location_name).first():
                db.add(ReferralLocationMaster(location_name=location_name))
        db.commit()
        print(f"✓ Referral locations seeded ({len(REFERRAL_LOCATIONS)})")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
