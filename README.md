stock-analysis
==============================
![Tests](https://github.com/jareducherek/stock-analysis/actions/workflows/tests.yml/badge.svg)
![Test Coverage](https://github.com/jareducherek/stock-analysis/blob/badges/master/test-coverage.svg)

Exploratory data analysis and machine learning techniques applied to time-series data associated with stock prices.

Installation instructions
==============================
- clone this repo, and either use make or run the commands manually in the Makefile:
```
make create_environment
conda activate stock-analysis
make requirements
```

Running
==============================
To activate the environment:
```
conda activate stock-analysis
```

To setup account details in .env file:
```
python src/utils/account_auth.py -h
```

To make a list of target tickers to scrape:
```
python src/data/get_tickers.py
```

To scrape Fidelity for those tickers:
```
python src/data/scrape_fidelity_analysts.py
```

To add scraped pickle files to MongoDB:
- add MongoDB key to .env file
```
python src/data/pickled_mongo.py
```

Developing
==============================
Some useful commands for after developing code for the repo:

MyPy:
```
mypy .
```

Flake8:
```
flake8 .
```

AutoPEP8:
Before finishing final changes, use `autopep8` to help reformat to standard.
```
autopep8 --in-place --recursive --aggressive --aggressive .
```

PyTest:
```
pytest -v --cov tests/
```



Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
