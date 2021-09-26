import pathlib
from pathlib import Path
import os

DIRNAME = os.path.dirname(__file__)

DATA_DIR = (Path(os.path.join(DIRNAME, '../../data/'))).resolve()
RAW_DIR = DATA_DIR / 'raw'
INTERIM_DIR = DATA_DIR / 'interim'
EXTERNAL_DIR= DATA_DIR / 'external'
PROCESSED_DIR = DATA_DIR / 'processed'
