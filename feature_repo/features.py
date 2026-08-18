from datetime import timedelta
from feast import Entity, FeatureView, Field, FileSource
from feast.types import Float32, Int64

student = Entity(
    name="student_id",
    join_keys=["student_id"],
    description="Unique student identifier.",
)

student_source = FileSource(
    name="student_skill_features_source",
    path="../data/processed/student_features.parquet",
    timestamp_field="event_timestamp",
)

student_skill_features = FeatureView(
    name="student_skill_features",
    entities=[student],
    ttl=timedelta(days=3650),
    schema=[
        Field(name="cgpa", dtype=Float32),
        Field(name="dsa_score", dtype=Int64),
        Field(name="system_design_score", dtype=Int64),
        Field(name="dbms_score", dtype=Int64),
        Field(name="oop_proficiency", dtype=Int64),
        Field(name="cloud_devops_score", dtype=Int64),
        Field(name="web_dev_score", dtype=Int64),
        Field(name="problem_solving_score", dtype=Float32),
        Field(name="aptitude_score", dtype=Int64),
        Field(name="communication_score", dtype=Float32),
        Field(name="teamwork_score", dtype=Int64),
        Field(name="github_projects_count", dtype=Int64),
        Field(name="internship_duration_months", dtype=Int64),
        Field(name="certifications_count", dtype=Int64),
        Field(name="hackathons_participated", dtype=Int64),
        Field(name="mock_interview_score", dtype=Int64),
        Field(name="curriculum_updated_year", dtype=Int64),
        Field(name="domain_code", dtype=Int64),
        Field(name="technical_skill_mean", dtype=Float32),
        Field(name="soft_skill_mean", dtype=Float32),
        Field(name="industry_exposure_score", dtype=Float32),
        Field(name="practical_experience_score", dtype=Float32),
        Field(name="curriculum_age_years", dtype=Int64),
    ],
    online=True,
    source=student_source,
    tags={"project": "curriculum-industry-skill-gap"},
)
