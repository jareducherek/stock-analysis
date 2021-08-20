# stock-analysis
Exploratory data analysis and machine learning techniques applied to time-series data associated with stock prices.

# Installation instructions
- clone this repo
- navigate to this repo and install required packages
- with make & anaconda instructions:
```
make create_environment
conda activate stock-analysis
make requirements
```
- otherwise, run the commands through Makefile manually to setup the env

# Running
```
conda activate stock-analysis
python get_tickers.py
python scrape_fidelity_analysts.py
```
