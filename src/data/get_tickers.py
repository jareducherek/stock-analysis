import bs4 as bs
import pickle
import requests

from src.utils.config import EXTERNAL_DIR
TARGET_PATH = EXTERNAL_DIR / 'sp500_tickers.txt'

def get_sp500_tickers(save = True):
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'id': 'constituents'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.find('td').text
        tickers.append(ticker.replace('\n', ''))

    if save:
        textfile = open(TARGET_PATH, "w")
        for element in tickers:
            textfile.write(element + "\n")
        textfile.close()

    return tickers

if __name__ == '__main__':
    get_sp500_tickers()
