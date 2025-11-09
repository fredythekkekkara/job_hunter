from dataclasses import dataclass, field
from typing import List, Optional

# ------------------ BASIC INFO ------------------ #
@dataclass
class BasicInfo:
    name: str
    title: str
    email: str
    phone: str
    location: str
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None
    summary: Optional[str] = None


# ------------------ EDUCATION ------------------ #
@dataclass
class EducationEntry:
    degree: str
    field: str
    institution: str
    location: str
    start_date: str
    end_date: str
    gpa: Optional[str] = None
    relevant_courses: List[str] = field(default_factory=list)


# ------------------ EXPERIENCE ------------------ #
@dataclass
class Experience:
    company: str
    position: str
    location: str
    start_date: str
    end_date: str
    achievements: List[str] = field(default_factory=list)


# ------------------ SKILLS ------------------ #
@dataclass
class Skills:
    programming_languages: List[str] = field(default_factory=list)
    data_technologies: List[str] = field(default_factory=list)
    databases: List[str] = field(default_factory=list)
    cloud_platforms: List[str] = field(default_factory=list)
    tools_and_frameworks: List[str] = field(default_factory=list)
    soft_skills: List[str] = field(default_factory=list)


# ------------------ CERTIFICATIONS & COURSES ------------------ #
@dataclass
class Certification:
    name: str
    issuer: str
    date: str

@dataclass
class Course:
    name: str
    platform: str
    completion_date: str


# ------------------ LANGUAGES ------------------ #
@dataclass
class LanguageEntry:
    name: str
    proficiency: str


# ------------------ PROFESSIONAL ------------------ #
@dataclass
class Professional:
    professional_interests: List[str] = field(default_factory=list)
    memberships: List[dict] = field(default_factory=list)


# ------------------ PUBLICATIONS ------------------ #
@dataclass
class Publication:
    title: str
    publisher: str
    date: str
    url: Optional[str] = None
    summary: Optional[str] = None


# ------------------ MAIN RESUME ------------------ #
@dataclass
class Resume:
    basic_info: Optional[BasicInfo] = None
    education: List[EducationEntry] = field(default_factory=list)
    experience: List[Experience] = field(default_factory=list)
    skills: Optional[Skills] = None
    certifications: List[Certification] = field(default_factory=list)
    courses: List[Course] = field(default_factory=list)
    languages: List[LanguageEntry] = field(default_factory=list)
    professional: Optional[Professional] = None
    publications: List[Publication] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)  # extracted from JD


# ------------------ JOB DESCRIPTION ------------------ #
@dataclass
class JobDescription:
    job_description: str