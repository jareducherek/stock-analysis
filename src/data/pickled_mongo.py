import pandas as pd
import pdb
import pickle
import json
from pymongo import MongoClient
import os
from tqdm import tqdm

client = MongoClient("mongodb+srv://master:YTJLdtq1ByQxE466@cluster0.cql3g.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

def mongo_eat_pkl(pkl_path, database, collection):
    """
    hungry hungry mongo
    """

    pkl_convert = pd.read_pickle(pkl_path)
    overview_cols = pd.read_pickle('../pickles/ticker_analyst_overview_column_names.pickle')
    historical_cols = pd.read_pickle('../pickles/ticker_specific_analyst_column_names.pickle')
    historical_dfs = []

    for i in pkl_convert:
        if len(i) != 9:
            tqdm.write(f'{collection} failed')
            return
        historical_dfs.append(i.pop())

    df = pd.DataFrame(pkl_convert, columns = overview_cols) #create dataframe
    coll = database[collection] #create collection
    ticker_docs = df.to_dict(orient = 'records')

    for i in range(len(ticker_docs)):
        historical_df = historical_dfs[i]
        url = historical_df.pop()
        ticker_docs[i]['Historical Data Url'] = url
        if len(historical_df) == 0:
            historical_df = pd.DataFrame(columns = historical_cols)
        else:
            historical_df = pd.DataFrame(historical_df, columns = historical_cols)
        ticker_docs[i]['Historical Data'] = historical_df.to_dict(orient = 'records')
    coll.insert_many(ticker_docs)

if __name__ == '__main__':
    database_name = 'stock_db'
    database = client[database_name] #create database
    coll_extension = '_data'
    curr_colls = database.list_collection_names()
    curr_colls = [x.split(coll_extension)[0] for x in curr_colls]

    ticker_files = os.listdir('../pickles/ticker_data/success/')
    ticker_files = [x.split('.pickle')[0] for x in ticker_files if 'pickle' in x]

    new_tickers = list(set(ticker_files) - set(curr_colls))
    tqdm.write(f'saving {len(new_tickers)} new tickers to Mongo...')
    for ticker_file in tqdm(new_tickers):
        mongo_eat_pkl(f'../pickles/ticker_data/success/{ticker_file}.pickle',
                      database, f'{ticker_file}{coll_extension}')
