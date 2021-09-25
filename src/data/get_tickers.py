import bs4 as bs
import pickle
import requests

def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'id': 'constituents'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.find('td').text
        tickers.append(ticker.replace('\n', ''))

    with open("../pickles/sp500tickers.pickle","wb") as f:
        pickle.dump(tickers, f)

    print(tickers)
    return tickers

if __name__ == '__main__':
    save_sp500_tickers()
