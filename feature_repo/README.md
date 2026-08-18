# Feast Repository

Run from this directory:

```bash
feast apply
```

Then from the project root:

```bash
python src/get_historical.py
python src/train_model.py
python src/materialize.py
python src/get_online.py
python src/predict.py
```

The FeatureView is defined in `features.py`.
