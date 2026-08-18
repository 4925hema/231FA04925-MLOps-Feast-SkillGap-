<<<<<<< HEAD
# Curriculum-Industry Skill Feature Store Using Feast

## Student Details
- **Name:** Hemanjaneyulu
- **Register Number:** `<YOUR_REGISTER_NUMBER>`
- **Section:** `<YOUR_SECTION>`
- **Required repository name:** `<RegisterNumber>MLOps-Feast-SkillGap`

> Replace the register number and section before submitting to GitHub.

## 1. Problem Statement
This project converts a curriculum-industry skill-gap dataset for 1,000 CSE students into a simple Feast feature store. The objective is to engineer reusable student-skill features, register them with Feast, retrieve historical features for model training, materialize them into an online SQLite store, retrieve online features, and use the same features in a machine-learning model to predict the **Skill_Gap_Index**.

The assignment requires demonstration of feature engineering, Feast entity/data source/FeatureView creation, `feast apply`, historical retrieval, materialization, online retrieval, ML usage, and GitHub documentation.

## 2. Dataset
- **Rows:** 1,000 students
- **Original columns:** 20
- **Domain specializations:** AI_ML, Cybersecurity, DataEngineering, DevOps, FullStack
- **Target:** `Skill_Gap_Index`
- **Entity:** `student_id` (derived from `Student_ID`)
- **How entries were created:** The supplied CSV is a synthetic/random student skill-gap dataset containing academic, technical, practical-experience, soft-skill, and industry-readiness variables.

### Original columns
`Student_ID`, `CGPA`, `DSA_Score`, `System_Design_Score`, `DBMS_Score`, `OOP_Proficiency`, `Cloud_DevOps_Score`, `Web_Dev_Score`, `Problem_Solving_Rating`, `Aptitude_Score`, `Communication_Rating`, `Teamwork_Score`, `Github_Projects_Count`, `Internship_Duration_Months`, `Certifications_Count`, `Hackathons_Participated`, `Mock_Interview_Score`, `Domain_Specialization`, `Curriculum_Updated_Year`, `Skill_Gap_Index`.

## 3. Data Cleaning
`src/prepare_data.py`:
1. Reads the supplied CSV.
2. Removes duplicate `Student_ID` values.
3. Converts numeric columns to numeric values.
4. Fills numeric missing values with the median.
5. Fills categorical missing values with the mode.
6. Creates `event_timestamp` for Feast.
7. Keeps `Skill_Gap_Index` outside the FeatureView to avoid target leakage.

## 4. Feature Engineering
The project creates reusable features:
- `cgpa`
- `dsa_score`
- `system_design_score`
- `dbms_score`
- `oop_proficiency`
- `cloud_devops_score`
- `web_dev_score`
- `problem_solving_score`
- `aptitude_score`
- `communication_score`
- `teamwork_score`
- `github_projects_count`
- `internship_duration_months`
- `certifications_count`
- `hackathons_participated`
- `mock_interview_score`
- `curriculum_updated_year`
- `domain_code`
- `technical_skill_mean`
- `soft_skill_mean`
- `industry_exposure_score`
- `practical_experience_score`
- `curriculum_age_years`

### Example feature calculation
`technical_skill_mean` is calculated as the mean of DSA, System Design, DBMS, OOP, Cloud/DevOps, and Web Development scores:

`technical_skill_mean = mean(DSA, System Design, DBMS, OOP, Cloud/DevOps, Web Development)`

`problem_solving_score` is normalized from the source scale by dividing `Problem_Solving_Rating` by 25. `communication_score` is converted from a 1–5 scale to approximately 0–100 by multiplying by 20.

## 5. Feast Architecture

```text
Original CSV Dataset
        |
        v
Data Cleaning + Feature Engineering
        |
        v
Parquet Offline Data + Labels
        |
        v
Feast FileSource
        |
        v
Feast FeatureView
        |
        +--------------------------+
        |                          |
        v                          v
Historical Retrieval         Materialization
        |                          |
        v                          v
Model Training               SQLite Online Store
                                   |
                                   v
                            Online Retrieval
                                   |
                                   v
                               Prediction
```

## 6. Feast Implementation

### Entity
The entity is `student_id`. It uniquely identifies one student and is used as the join key for feature retrieval.

### Data source
The Feast `FileSource` points to `data/processed/student_features.parquet`. The source contains `event_timestamp` so Feast can perform point-in-time historical retrieval.

### FeatureView
`student_skill_features` contains the reusable student academic, technical, soft-skill, practical-experience, and engineered features listed above. `Skill_Gap_Index` is deliberately not included as a feature because it is the prediction target.

### Historical retrieval
`src/get_historical.py` calls `get_historical_features()` using student IDs and timestamps. This produces the point-in-time feature set used by the model.

### Model
`src/train_model.py` trains a `RandomForestRegressor` to predict `Skill_Gap_Index`. The train/test split uses `random_state=42` and a 20% test set. Metrics are saved to `outputs/model_metrics.json`.

### Materialization
`src/materialize.py` calls Feast materialization for the available event-time range. This copies the latest feature values into the online SQLite store.

### Online retrieval
`src/get_online.py` calls `get_online_features()` for a student such as `CSE_0001`.

### Prediction
`src/predict.py` retrieves the same Feast feature vector online and sends it to the saved model.

## 7. Required Questions

### 1. What is the entity?
`student_id`, representing one student.

### 2. List the features stored in the FeatureView.
The FeatureView stores the 24 features listed in the Feature Engineering section.

### 3. Explain how one feature was calculated.
`technical_skill_mean` is the arithmetic mean of six technical skill scores: DSA, System Design, DBMS, OOP, Cloud/DevOps, and Web Development.

### 4. Difference between original dataset and feature dataset
The original dataset contains raw student attributes and the target. The feature dataset contains cleaned, model-ready numerical features, a Feast entity key, and an event timestamp. The target is kept separately for supervised learning and is not registered as an input feature.

### 5. Purpose of the offline store
The offline store keeps historical feature data and supports point-in-time retrieval for training and analysis.

### 6. Purpose of the online store
The online store keeps the latest feature values so applications can retrieve features quickly for prediction.

### 7. Purpose of `feast apply`
`feast apply` registers or updates the Feast entities, data sources, and FeatureViews in the feature repository.

### 8. What does materialization do?
Materialization loads feature values from the offline source into the online store for the specified time range.

### 9. Advantage of Feast over manually calculating features
The same centrally defined feature transformations can be reused for training and inference. This reduces duplicated feature logic and helps keep training and serving features consistent.

### 10. Two limitations of the current dataset
1. The dataset is synthetic/random and may not represent real hiring or curriculum evidence.
2. The dataset is a single snapshot rather than a rich longitudinal record of how a student's skills change over time.

### 11. Two improvements when more evidence is available
1. Add time-versioned curriculum outcomes, placement outcomes, job descriptions, interview results, and industry skill-demand evidence.
2. Add richer domain-specific features and production monitoring such as feature freshness, drift detection, data quality checks, and model performance tracking.

## 8. Run the Project

### Environment
Python 3.10/3.11 is recommended.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

### Step 1: Prepare data
```bash
python src/prepare_data.py
```

### Step 2: Register Feast objects
=======
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

>>>>>>> 6e7843b80dfd8eb1fc8edf186317de2c56620d54
```bash
cd feature_repo
feast apply
cd ..
```

<<<<<<< HEAD
### Step 3: Historical retrieval
=======
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

>>>>>>> 6e7843b80dfd8eb1fc8edf186317de2c56620d54
```bash
python src/get_historical.py
```

<<<<<<< HEAD
### Step 4: Train model
=======
### Step 4 — Train Model

>>>>>>> 6e7843b80dfd8eb1fc8edf186317de2c56620d54
```bash
python src/train_model.py
```

<<<<<<< HEAD
### Step 5: Materialize online store
=======
### Step 5 — Materialize Online Store

>>>>>>> 6e7843b80dfd8eb1fc8edf186317de2c56620d54
```bash
python src/materialize.py
```

<<<<<<< HEAD
### Step 6: Online retrieval
=======
### Step 6 — Online Retrieval

>>>>>>> 6e7843b80dfd8eb1fc8edf186317de2c56620d54
```bash
python src/get_online.py
```

<<<<<<< HEAD
### Step 7: Final prediction
=======
### Step 7 — Prediction

>>>>>>> 6e7843b80dfd8eb1fc8edf186317de2c56620d54
```bash
python src/predict.py
```

<<<<<<< HEAD
## 9. Expected Deliverables
- `data/processed/student_features.parquet`
- `data/processed/training_labels.parquet`
- Feast registry
- SQLite online store
- historical feature output
- trained model
- model metrics
- online feature output
- final prediction
- architecture diagram
- this README


## 9. Reference Results from the Supplied Dataset
A reference Random Forest run using the same engineered feature columns gives:
- **MAE:** 4.3342
- **RMSE:** 5.7924
- **R²:** 0.7827
- **Train/Test:** 800 / 200
- **Reference prediction for CSE_0001:** Skill_Gap_Index ≈ 8.30

These reference numbers are included so the repository has an immediate result. The formal Feast workflow should still be executed locally after installing Feast and PyArrow; the Feast-generated historical/online outputs may vary with the installed Feast version.

## 10. Submission
Create a GitHub repository named:

`<RegisterNumber>MLOps-Feast-SkillGap`

Push the complete project and submit the repository link through the faculty Google Form.
=======
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
## 📸 Project Report Images

### Dataset Profile

![Dataset Profile](images/01_dataset_profile.png)

### Data Visualization

![Data Visualization](images/02_data_visualization.png)

### Feast Architecture

![Feast Architecture](images/03_feast_architecture.jpeg)

### Project Output

![Project Output](images/04_project_output.png)
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
>>>>>>> 6e7843b80dfd8eb1fc8edf186317de2c56620d54
