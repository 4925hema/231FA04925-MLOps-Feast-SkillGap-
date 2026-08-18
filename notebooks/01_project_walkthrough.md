# Project Walkthrough

This folder contains the assignment workflow in executable script order.

1. `src/prepare_data.py` — clean and engineer features.
2. `feast apply` — register entity, source and FeatureView.
3. `src/get_historical.py` — retrieve point-in-time features.
4. `src/train_model.py` — train RandomForestRegressor.
5. `src/materialize.py` — load latest features into SQLite.
6. `src/get_online.py` — retrieve serving features.
7. `src/predict.py` — make final prediction.

The main README contains the required assignment questions and explanations.
