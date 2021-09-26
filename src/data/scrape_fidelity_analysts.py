from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as exceptions

import os
import pickle
import time
from datetime import datetime
from tqdm import tqdm
from pymongo import MongoClient

from account_auth import get_login
user, pw = get_login('../authentication/')


def fidelity_login():
    """
    Log into fidelity
    """
    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('detach', True)
    options.add_argument('--log-level=3')
    # options.add_experiemntal_option('useAutomationExtension', False)
    driver = webdriver.Chrome(
        options=options,
        executable_path='../chromedriver.exe')

    driver.get('https://www.fidelity.com/')
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'input#userId-input'))).send_keys(user)
    time.sleep(1)
    driver.find_element_by_css_selector('input#password').send_keys(pw)
    time.sleep(1)
    driver.find_element_by_css_selector('button#fs-login-button').click()
    time.sleep(10)

    return driver


def scrape_overview_data(driver, dropdown):
    dropdown.select_by_visible_text('Current Firm Opinion')
    table_id = '@id="allOpinionsTable"'
    tablebot_id = '@id="bottom-table"'

    col_eles = driver.find_elements_by_xpath(
        f'//table[{table_id}]/thead/tr/th')
    num_cols = len(col_eles)
    row_eles = driver.find_elements_by_xpath(f'//table[{table_id}]/tbody/tr')
    num_rows = len(row_eles)
    bottom_rows = driver.find_elements_by_xpath(
        f'//table[{tablebot_id}]/tbody/tr')
    num_bot_rows = len(bottom_rows)

    table = []
    # add each row to the table
    for i in range(num_rows):
        row = []
        for j in range(num_cols):
            # getting text from the ith row and jth column
            row.append(driver.find_element_by_xpath(
                f'//table[{table_id}]/tbody/tr[{i + 1}]/td[{j + 1}]').text)
        table.append(row)
    for i in range(num_bot_rows):
        row = []
        for j in range(num_cols):
            # getting text from the ith row and jth column
            row.append(driver.find_element_by_xpath(
                f'//table[{tablebot_id}]/tbody/tr[{i + 1}]/td[{j + 1}]').text)
        table.append(row)

    # change select option, add the new data to the current table
    dropdown.select_by_visible_text('Last Opinion Change')
    for i in range(num_rows):
        # iterate over the new columns
        for j in (5, 6):
            table[i][j] = driver.find_element_by_xpath(
                f'//table[{table_id}]/tbody/tr[{i + 1}]/td[{j + 1}]').text
    offset = i + 1
    for k in range(num_bot_rows):
        # iterate over the new columns
        for j in (5, 6):
            table[offset + k][j] = driver.find_element_by_xpath(
                f'//table[{tablebot_id}]/tbody/tr[{k + 1}]/td[{j + 1}]').text

    # clean up strings in our table
    for i in range(len(table)):
        table[i][0] = table[i][0].replace(' (i)', '')
        table[i].pop(2)

    urls = []
    for i in range(num_rows):
        # get url from appropriate attrirbute in table, add tag '&view=3' for 3
        # year view
        d = driver.find_element_by_xpath(
            f'//table[{table_id}]/tbody/tr[{i + 1}]')
        urls.append(d.find_element_by_tag_name(
            'a').get_attribute('href') + '&view=3')
    for i in range(num_bot_rows):
        d = driver.find_element_by_xpath(
            f'//table[{tablebot_id}]/tbody/tr[{i + 1}]')
        urls.append(d.find_element_by_tag_name(
            'a').get_attribute('href') + '&view=3')

    return table, urls


def scrape_individual_data(driver):

    table_jsid = '@jsid="smartsentiment-performance-data-table-performance"'
    WebDriverWait(
        driver, 15).until(
        EC.presence_of_element_located(
            (By.XPATH, f'//table[{table_jsid}]')))

    col_eles = driver.find_elements_by_xpath(
        f'//table[{table_jsid}]/thead/tr/th')
    num_cols = len(col_eles)
    row_eles = driver.find_elements_by_xpath(f'//table[{table_jsid}]/tbody/tr')
    num_rows = len(row_eles)

    sub_table = []
    # add each row to the table
    for i in range(num_rows):
        row = []
        for j in range(num_cols):
            # getting text from the ith row and jth column
            row.append(driver.find_element_by_xpath(
                f'//table[{table_jsid}]/tbody/tr[{i + 1}]/td[{j + 1}]').text)
        sub_table.append(row)

    return sub_table


def scrape_analyst_data(driver, ticker):
    driver.get(
        f'https://snapshot.fidelity.com/fidresearch/snapshot/landing.jhtml#/analystsopinions?symbol={ticker.replace(".", "/")}')
    # sleep for at least 7 seconds, then wait to load fully
    time.sleep(7)
    try:
        dropdown = Select(
            WebDriverWait(
                driver, 15).until(
                EC.presence_of_element_located(
                    (By.ID, 'firm'))))
    except exceptions.TimeoutException:
        error = f'analyst site did not load: {ticker}'
        tqdm.write(error)
        with open(f'../pickles/ticker_data/no_load/{ticker}.pickle', 'wb') as f:
            pickle.dump(error, f)
        return driver

    try:
        table, urls = scrape_overview_data(driver, dropdown)
    except BaseException:
        error = f'analyst scraping failed: {ticker}'
        with open(f'../pickles/ticker_data/failed/{ticker}.pickle', 'wb') as f:
            pickle.dump(error, f)
        tqdm.write(error)
        return driver

    full_table = table
    error = False
    for i, url in enumerate(urls):
        sub_table = []
        flag = False
        try:
            # go to url if opinion change is within 3 year period
            flag = (
                datetime.now() - datetime.strptime(full_table[i][4], '%m/%d/%y')).days < 3 * 366
        except BaseException:
            pass
        if flag:
            driver.get(url)
            # sleep for at least 7 seconds, then wait to load fully
            time.sleep(7)
            try:
                sub_table = scrape_individual_data(driver)
            except BaseException:
                error = True
                tqdm.write(f'specific analyst scraping failed: {ticker}')
        sub_table.append(url)
        full_table[i] += [sub_table]

    if error:
        name = f'../pickles/ticker_data/error/{ticker}.pickle'
    else:
        name = f'../pickles/ticker_data/success/{ticker}.pickle'
    with open(name, 'wb') as f:
        pickle.dump(full_table, f)

    return driver


if __name__ == '__main__':
    with open('../pickles/sp500tickers.pickle', 'rb') as f:
        tickers = pickle.load(f)

    finished_tickers = [x.split('.')[0] for x in os.listdir(
        '../pickles/ticker_data/success/') if 'pickle' in x]
    tickers = [x for x in tickers if x not in finished_tickers]
    print(f'starting scraping {len(tickers)} tickers from fidelity')

    start = datetime.now()
    driver = fidelity_login()
    for ticker in tqdm(tickers):
        cur = datetime.now()
        elapsed = cur - start
        # if more than 2 hours elapsed
        if elapsed.days * 24 + elapsed.seconds // 3600 > 2:
            start = cur
            driver.close()
            time.sleep(7)
            driver = fidelity_login()
        driver = scrape_analyst_data(driver, ticker)
    driver.close()
    print('finished!')
