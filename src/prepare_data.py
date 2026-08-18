from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "skill_gap_students.csv"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

DOMAIN_MAP = {
    "AI_ML": 0,
    "Cybersecurity": 1,
    "DataEngineering": 2,
    "DevOps": 3,
    "FullStack": 4,
}

NUMERIC_COLUMNS = [
    "CGPA", "DSA_Score", "System_Design_Score", "DBMS_Score",
    "OOP_Proficiency", "Cloud_DevOps_Score", "Web_Dev_Score",
    "Problem_Solving_Rating", "Aptitude_Score", "Communication_Rating",
    "Teamwork_Score", "Github_Projects_Count", "Internship_Duration_Months",
    "Certifications_Count", "Hackathons_Participated", "Mock_Interview_Score",
    "Curriculum_Updated_Year", "Skill_Gap_Index",
]

def main():
    df = pd.read_csv(RAW)

    # Basic cleaning
    df = df.drop_duplicates(subset=["Student_ID"]).copy()
    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].fillna(df[col].median())

    df["Domain_Specialization"] = (
        df["Domain_Specialization"].fillna(df["Domain_Specialization"].mode()[0])
    )

    # Feast entity
    df["student_id"] = df["Student_ID"].astype(str)

    # One timestamp per student for this snapshot dataset.
    df["event_timestamp"] = pd.Timestamp("2026-01-01", tz="UTC")

    # Feature engineering
    df["problem_solving_score"] = df["Problem_Solving_Rating"] / 25.0
    df["communication_score"] = df["Communication_Rating"] * 20.0

    technical_cols = [
        "DSA_Score", "System_Design_Score", "DBMS_Score",
        "OOP_Proficiency", "Cloud_DevOps_Score", "Web_Dev_Score"
    ]
    df["technical_skill_mean"] = df[technical_cols].mean(axis=1)

    df["soft_skill_mean"] = df[
        ["communication_score", "Teamwork_Score", "Problem_Solving_Rating"]
    ].assign(Problem_Solving_Rating=lambda x: x["Problem_Solving_Rating"] / 25.0).mean(axis=1)

    # Normalize practical/industry evidence to roughly 0-100.
    df["industry_exposure_score"] = (
        (df["Internship_Duration_Months"] / 12.0) * 30
        + (df["Certifications_Count"] / 5.0) * 20
        + (df["Hackathons_Participated"] / 8.0) * 20
        + (df["Github_Projects_Count"] / 15.0) * 30
    ).clip(0, 100)

    df["practical_experience_score"] = (
        (df["Github_Projects_Count"] / 15.0) * 35
        + (df["Internship_Duration_Months"] / 12.0) * 35
        + (df["Hackathons_Participated"] / 8.0) * 30
    ).clip(0, 100)

    df["curriculum_age_years"] = (2026 - df["Curriculum_Updated_Year"]).clip(lower=0)
    df["domain_code"] = df["Domain_Specialization"].map(DOMAIN_MAP).fillna(-1).astype(int)

    feature_columns = [
        "student_id", "event_timestamp",
        "CGPA", "DSA_Score", "System_Design_Score", "DBMS_Score",
        "OOP_Proficiency", "Cloud_DevOps_Score", "Web_Dev_Score",
        "problem_solving_score", "Aptitude_Score", "communication_score",
        "Teamwork_Score", "Github_Projects_Count", "Internship_Duration_Months",
        "Certifications_Count", "Hackathons_Participated", "Mock_Interview_Score",
        "Curriculum_Updated_Year", "domain_code", "technical_skill_mean",
        "soft_skill_mean", "industry_exposure_score",
        "practical_experience_score", "curriculum_age_years",
    ]

    rename = {
        "CGPA": "cgpa", "DSA_Score": "dsa_score",
        "System_Design_Score": "system_design_score", "DBMS_Score": "dbms_score",
        "OOP_Proficiency": "oop_proficiency", "Cloud_DevOps_Score": "cloud_devops_score",
        "Web_Dev_Score": "web_dev_score", "Aptitude_Score": "aptitude_score",
        "Teamwork_Score": "teamwork_score", "Github_Projects_Count": "github_projects_count",
        "Internship_Duration_Months": "internship_duration_months",
        "Certifications_Count": "certifications_count",
        "Hackathons_Participated": "hackathons_participated",
        "Mock_Interview_Score": "mock_interview_score",
        "Curriculum_Updated_Year": "curriculum_updated_year",
    }

    features = df[feature_columns].rename(columns=rename)
    labels = df[["student_id", "event_timestamp", "Skill_Gap_Index"]].rename(
        columns={"Skill_Gap_Index": "skill_gap_index"}
    )

    features.to_parquet(OUT / "student_features.parquet", index=False)
    labels.to_parquet(OUT / "training_labels.parquet", index=False)
    df.to_csv(OUT / "cleaned_dataset.csv", index=False)

    print("Prepared dataset:", len(df), "students")
    print("Feature columns:", len(features.columns) - 2)
    print("Saved:", OUT / "student_features.parquet")
    print("Saved:", OUT / "training_labels.parquet")

if __name__ == "__main__":
    main()
