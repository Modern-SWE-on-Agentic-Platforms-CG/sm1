from pydantic import BaseModel, EmailStr
from typing import Optional


class ReferralTechOut(BaseModel):
    id: int
    tech_name: str
    model_config = {"from_attributes": True}


class ReferralNoticePeriodOut(BaseModel):
    id: int
    notice_period: str
    model_config = {"from_attributes": True}


class ReferralLocationOut(BaseModel):
    id: int
    location_name: str
    model_config = {"from_attributes": True}


class ReferralCandidateCreate(BaseModel):
    candidate_name: str
    email: str
    phone: Optional[str] = None
    technology_id: Optional[int] = None
    notice_period_id: Optional[int] = None
    location_id: Optional[int] = None
    experience_years: Optional[float] = None
    current_company: Optional[str] = None
    current_ctc: Optional[float] = None
    expected_ctc: Optional[float] = None
    referred_by_emp_id: Optional[int] = None
    bu: Optional[str] = None
    account: Optional[str] = None


class ReferralCandidateOut(BaseModel):
    referral_candidate_id: int
    candidate_name: str
    email: str
    phone: Optional[str] = None
    experience_years: Optional[float] = None
    current_company: Optional[str] = None
    current_ctc: Optional[float] = None
    expected_ctc: Optional[float] = None
    status: Optional[str] = None
    bu: Optional[str] = None
    account: Optional[str] = None
    model_config = {"from_attributes": True}


class ReferralSkillCreate(BaseModel):
    skill_name: str


class ReferralSkillOut(BaseModel):
    id: int
    skill_name: str
    model_config = {"from_attributes": True}
