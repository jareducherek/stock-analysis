import pytest
from src.data.get_tickers import get_sp500_tickers


def test_get_sp500_tickers():

    test_tickers = ['AAPL', 'AMZN', 'GOOGL', 'PEP', 'V', 'RTX']
    tickers = get_sp500_tickers(save=False)

    for ticker in test_tickers:
        assert ticker in tickers
