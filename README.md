# 231FA04925-MLOps-Feast-SkillGap-
# MLOps-Feast-SkillGap

## Curriculum-Industry Skill Feature Store Using Feast

**MLOps • Feature Engineering • Feast • Historical Retrieval • Online Store • Machine Learning**

---

## 👨‍🎓 Student Details

| Details                    | Information                   |
| -------------------------- | ----------------------------- |
| **Name**                   | P.HEMANJANEYULU               |
| **Register Number**        | 231FA04925                    |
| **Section**                | 15                            |
| **Dataset**                | CSE Student Skill-Gap Dataset |
| **Records**                | 1,000                         |
| **Target**                 | `Skill_Gap_Index`             |
| **Feature Store**          | Feast                         |
| **Online Store**           | SQLite                        |
| **Machine Learning Model** | RandomForestRegressor         |

---

## 📌 Project Overview

This project converts a **1,000-student curriculum-industry skill-gap dataset** into a reusable **Feast Feature Store** and connects it to a machine-learning workflow.

The project demonstrates:

* Data cleaning
* Feature engineering
* Feast entity creation
* Feast `FileSource`
* Feast `FeatureView`
* Historical feature retrieval
* Online feature materialization
* SQLite online store
* Online feature retrieval
* Random Forest regression
* GitHub documentation

The main MLOps objective is **feature consistency**. The same centrally defined features are reused during model training and prediction instead of duplicating transformation logic in separate scripts.

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │   Raw CSV Dataset   │
                    │   1,000 Students    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Data Preparation  │
                    │  Feature Engineering│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Processed Features  │
                    │       Parquet       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       Feast         │
                    │   Feature Store     │
                    └───────┬─────┬───────┘
                            │     │
              Historical   │     │   Materialization
              Retrieval    │     │
                            ▼     ▼
                    ┌──────────┐ ┌──────────────┐
                    │ Offline  │ │ SQLite Online│
                    │  Store   │ │    Store     │
                    └────┬─────┘ └──────┬───────┘
                         │              │
                         ▼              ▼
                  ┌────────────┐  ┌─────────────┐
                  │ Model      │  │ Prediction  │
                  │ Training   │  │   Serving   │
                  └─────┬──────┘  └──────┬──────┘
                        │                │
                        └───────┬────────┘
                                ▼
                    ┌─────────────────────┐
                    │ Skill_Gap_Index     │
                    │     Prediction      │
                    └─────────────────────┘
```

The architecture separates raw-data preparation from feature serving. Historical retrieval supports point-in-time training, while materialization moves the latest values into the SQLite online store for prediction-time retrieval.

---

## 📊 Dataset

The dataset contains **1,000 student records** and **20 original columns**.

### Original Columns

```text
Student_ID
CGPA
DSA_Score
System_Design_Score
DBMS_Score
OOP_Proficiency
Cloud_DevOps_Score
Web_Dev_Score
Problem_Solving_Rating
Aptitude_Score
Communication_Rating
Teamwork_Score
Github_Projects_Count
Internship_Duration_Months
Certifications_Count
Hackathons_Participated
Mock_Interview_Score
Domain_Specialization
Curriculum_Updated_Year
Skill_Gap_Index
```

### Domains

```text
AI_ML
Cybersecurity
DataEngineering
DevOps
FullStack
```

The dataset is described in the project report as synthetic/random and includes academic, technical, practical-experience, soft-skill, and industry-readiness variables.

---

## 🧹 Data Cleaning & Feature Engineering

The data preparation pipeline performs the following operations:

1. Reads the supplied CSV dataset.
2. Removes duplicate student IDs.
3. Converts numeric columns to numeric types.
4. Fills missing numeric values using the median.
5. Fills missing categorical values using the mode.
6. Creates an `event_timestamp` required by Feast.
7. Separates `Skill_Gap_Index` from the feature set to prevent target leakage.

---

## ⚙️ Engineered Features

The Feast FeatureView contains reusable academic, technical, soft-skill, practical-experience, and curriculum features.

Important engineered features include:

| Feature                      | Description                                    |
| ---------------------------- | ---------------------------------------------- |
| `technical_skill_mean`       | Mean of six technical skill scores             |
| `soft_skill_mean`            | Mean soft-skill indicator                      |
| `industry_exposure_score`    | Industry exposure composite                    |
| `practical_experience_score` | Practical experience composite                 |
| `curriculum_age_years`       | Age of curriculum relative to project snapshot |
| `domain_code`                | Encoded domain specialization                  |

### Example Feature Calculation

```python
technical_skill_mean = mean(
    DSA,
    System Design,
    DBMS,
    OOP,
    Cloud/DevOps,
    Web Development
)
```

Other transformations include:

```python
problem_solving_score = Problem_Solving_Rating / 25
communication_score = Communication_Rating * 20
```

`Skill_Gap_Index` is kept outside the FeatureView because it is the supervised-learning target.

---

## 🧩 Feast Feature Store

### Entity

The Feast entity is:

```text
student_id
```

It uniquely identifies a student and acts as the join key for feature retrieval.

### FileSource

The Feast `FileSource` uses the processed Parquet file:

```text
data/processed/student_features.parquet
```

with:

```text
event_timestamp
```

as the timestamp field.

### FeatureView

The FeatureView is:

```text
student_skill_features
```

It contains the reusable student skill features while excluding the target variable.

---

## 🔧 Feast Configuration

Example Feast implementation:

```python
student = Entity(
    name="student_id",
    join_keys=["student_id"],
    description="Unique student identifier."
)

student_source = FileSource(
    name="student_skill_features_source",
    path="../data/processed/student_features.parquet",
    timestamp_field="event_timestamp"
)

student_skill_features = FeatureView(
    name="student_skill_features",
    entities=[student],
    ttl=timedelta(days=3650),
    online=True,
    source=student_source
)
```

---

## 🚀 Feast Apply

Register the Feast objects using:

```bash
cd feature_repo
feast apply
cd ..
```

`feast apply` registers or updates the configured Feast entities, data sources, and FeatureViews.

---

## 🕐 Historical Feature Retrieval

Historical retrieval creates point-in-time correct features for machine-learning training.

Example:

```python
store.get_historical_features(
    entity_df=entity_df,
    features=[
        "student_skill_features:cgpa",
        "student_skill_features:dsa_score",
        "student_skill_features:technical_skill_mean"
    ]
)
```

This prevents future feature values from incorrectly leaking into historical training data.

---

## 💾 Online Store

The project uses **SQLite** as the Feast online store.

Materialization loads the latest feature values from the offline source into the online store.

Example:

```python
store.materialize(
    start_date=start_date,
    end_date=end_date
)
```

Online retrieval can then obtain the current feature vector for a student.

---

## 🔎 Online Retrieval Example

Example student:

```text
CSE_0001
```

Selected online feature values:

| Feature                    |  Value |
| -------------------------- | -----: |
| CGPA                       |   6.87 |
| DSA Score                  |   46.0 |
| Mock Interview Score       |   86.0 |
| Domain Code                |    3.0 |
| Technical Skill Mean       |   39.0 |
| Soft Skill Mean            | 56.907 |
| Industry Exposure Score    |   51.0 |
| Practical Experience Score |   48.0 |
| Curriculum Age             |    3.0 |

---

## 🤖 Machine Learning Model

The project uses:

```text
RandomForestRegressor
```

### Target

```text
Skill_Gap_Index
```

### Train/Test Split

```text
Training rows: 800
Testing rows: 200
Split: 80% / 20%
random_state: 42
```

---

## 📈 Model Results

Reference results from the project:

| Metric   |  Value |
| -------- | -----: |
| **MAE**  | 4.3342 |
| **RMSE** | 5.7924 |
| **R²**   | 0.7827 |

### Interpretation

* **MAE = 4.3342** — average absolute prediction error.
* **RMSE = 5.7924** — gives greater penalty to larger errors.
* **R² = 0.7827** — indicates the explained variance on the reference test set.

These are reference project results and the complete workflow should be executed locally after installing dependencies.

---

## 🎯 Sample Prediction

For student:

```text
CSE_0001
```

The reference prediction is:

```text
Predicted Skill_Gap_Index: 8.30
```

---

## ❓ Assignment Analysis

### 1. What is the entity in the Feast implementation?

The entity is:

```text
student_id
```

It uniquely identifies a student and is used as the join key for feature retrieval.

### 2. What features are stored in the FeatureView?

```text
cgpa
dsa_score
system_design_score
dbms_score
oop_proficiency
cloud_devops_score
web_dev_score
problem_solving_score
aptitude_score
communication_score
teamwork_score
github_projects_count
internship_duration_months
certifications_count
hackathons_participated
mock_interview_score
curriculum_updated_year
domain_code
technical_skill_mean
soft_skill_mean
industry_exposure_score
practical_experience_score
curriculum_age_years
```

### 3. How is one feature calculated?

`technical_skill_mean` is calculated as the arithmetic mean of:

```text
DSA
System Design
DBMS
OOP
Cloud/DevOps
Web Development
```

### 4. What is the difference between the original dataset and feature dataset?

The original dataset contains raw student attributes and the target.

The processed feature dataset contains:

* Cleaned numerical features
* Feast entity key
* Event timestamp
* Engineered features

The target `Skill_Gap_Index` is kept separately for supervised learning.

### 5. What is the purpose of the offline store?

The offline store keeps historical feature data and supports point-in-time retrieval for training and analysis.

### 6. What is the purpose of the online store?

The online store keeps the latest feature values so applications can retrieve features quickly during prediction.

### 7. What is the purpose of `feast apply`?

It registers or updates:

* Entities
* Data sources
* FeatureViews

in the Feast registry.

### 8. What does materialization do?

Materialization loads feature values from the offline source into the online store for a specified time range.

### 9. Why use Feast instead of calculating features separately?

Feast allows the same centrally defined feature transformations to be reused during training and inference. This reduces duplicated logic and improves training-serving consistency.

### 10. What are two limitations?

1. The dataset is synthetic/random and may not represent real hiring or curriculum evidence.
2. The dataset is primarily a single snapshot rather than a longitudinal record of student skill development.

### 11. How can the Feature Store be improved?

Future improvements include:

* Time-versioned curriculum outcomes
* Placement outcomes
* Job descriptions
* Interview results
* Industry skill-demand data
* Richer domain-specific features
* Feature freshness monitoring
* Feature drift detection
* Data-quality checks
* Model-performance monitoring

---

## 📁 Project Structure

```text
MLOps-Feast-SkillGap/
│
├── README.md
├── requirements.txt
│
├── feature_repo/
│   ├── feature_store.yaml
│   └── features.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── prepare_data.py
│   ├── get_historical.py
│   ├── train_model.py
│   ├── materialize.py
│   ├── get_online.py
│   └── predict.py
│
├── outputs/
│   ├── model_metrics.json
│   ├── online_features_sample.json
│   └── historical_features_sample.csv
│
├── models/
│   └── skill_gap_model.joblib
│
├── tests/
│   └── test_prepare_data.py
│
└── notebooks/
```

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd MLOps-Feast-SkillGap
```

### 2. Create Virtual Environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Linux/macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Project

Run the scripts in the following order.

### Step 1 — Prepare Data

```bash
python src/prepare_data.py
```

### Step 2 — Apply Feast

```bash
cd feature_repo
feast apply
cd ..
```

### Step 3 — Historical Retrieval

```bash
python src/get_historical.py
```

### Step 4 — Train Model

```bash
python src/train_model.py
```

### Step 5 — Materialize Online Store

```bash
python src/materialize.py
```

### Step 6 — Online Retrieval

```bash
python src/get_online.py
```

### Step 7 — Prediction

```bash
python src/predict.py
```

---

## 🧪 Testing

Run the data-preparation tests:

```bash
pytest
```

The project includes basic data-preparation test coverage in:

```text
tests/test_prepare_data.py
```

---

## 📸 Screenshots

You can add screenshots of your project to GitHub by creating an `images` folder:

```text
MLOps-Feast-SkillGap/
└── images/
    ├── architecture.png
    ├── feast-apply.png
    ├── historical-retrieval.png
    ├── online-store.png
    └── prediction.png
```

Then display them in this README using:

```markdown
## 📸 Project Screenshots

### Feast Architecture

![Feast Architecture](images/architecture.png)

### Feast Apply

![Feast Apply](images/feast-apply.png)

### Historical Retrieval

![Historical Retrieval](images/historical-retrieval.png)

### Online Store

![Online Store](images/online-store.png)

### Prediction

![Prediction](images/prediction.png)
```

---

## 📌 Key Project Files

| File                                     | Purpose                                       |
| ---------------------------------------- | --------------------------------------------- |
| `README.md`                              | Project documentation and assignment analysis |
| `feature_repo/features.py`               | Feast Entity, FileSource and FeatureView      |
| `feature_repo/feature_store.yaml`        | Feast repository configuration                |
| `src/prepare_data.py`                    | Data cleaning and feature engineering         |
| `src/get_historical.py`                  | Historical feature retrieval                  |
| `src/train_model.py`                     | Random Forest training and metrics            |
| `src/materialize.py`                     | Online store materialization                  |
| `src/get_online.py`                      | Online feature retrieval                      |
| `src/predict.py`                         | Feature retrieval and prediction              |
| `outputs/model_metrics.json`             | Model metrics                                 |
| `outputs/online_features_sample.json`    | Online feature example                        |
| `outputs/historical_features_sample.csv` | Historical feature output                     |
| `models/skill_gap_model.joblib`          | Trained model                                 |
| `tests/test_prepare_data.py`             | Data-preparation tests                        |

---

## ⚠️ Limitations

The current dataset has the following limitations:

* Synthetic/random records may not fully represent real student outcomes.
* It may not accurately represent job-market requirements.
* It is primarily a single snapshot.
* It provides limited evidence about skill progression over time.

---

## 🔮 Future Improvements

The Feature Store can be improved by adding:

```text
Industry skill-demand data
Curriculum outcomes
Placement results
Internship outcomes
Job descriptions
Interview results
Domain-specific features
Data-quality validation
Feature freshness monitoring
Feature drift detection
Model monitoring
Automated alerting
```

A future production architecture could also replace the local FileSource + SQLite setup with production-grade offline and online stores.

---

## 🚀 MLOps Maturity Path

```text
Level 1 → Repeatable
    Manual but scripted data preparation and training

Level 2 → Feature Reuse
    Central Feast definitions reused for training and inference

Level 3 → Production Monitoring
    Data quality, freshness, drift and model monitoring

Level 4 → Automated Delivery
    CI/CD, automated training, registry promotion and rollback

Level 5 → Continuous Learning
    Scheduled/event-driven retraining using new evidence
```

---

## 📋 Assignment Requirements Covered

| Requirement          | Status                     |
| -------------------- | -------------------------- |
| Feature Engineering  | ✅ Completed                |
| Feast Entity         | ✅ `student_id`             |
| Feast Data Source    | ✅ FileSource               |
| FeatureView          | ✅ `student_skill_features` |
| `feast apply`        | ✅ Implemented              |
| Historical Retrieval | ✅ Implemented              |
| Materialization      | ✅ Implemented              |
| Online Retrieval     | ✅ Implemented              |
| Machine Learning     | ✅ RandomForestRegressor    |
| GitHub Documentation | ✅ This README              |

---

## 📊 Final Result

The project demonstrates a complete student-skill feature pipeline:

```text
Raw Student Data
       ↓
Data Cleaning
       ↓
Feature Engineering
       ↓
Feast Feature Store
       ↓
Historical Retrieval
       ↓
Random Forest Training
       ↓
Model Evaluation
       ↓
Materialization
       ↓
SQLite Online Store
       ↓
Online Feature Retrieval
       ↓
Skill Gap Prediction
```

The reference model results are:

```text
MAE  = 4.3342
RMSE = 5.7924
R²   = 0.7827
```

Reference prediction:

```text
Student: CSE_0001
Predicted Skill_Gap_Index: 8.30
```

---

## 👨‍💻 Author

**P.HEMANJANEYULU**

**Register Number:** 231FA04925

**Section:** 15

---

## 📚 Project Documentation

This README is based on the submitted project report and follows the assignment requirements for the **Curriculum-Industry Skill Feature Store Using Feast** project.
