from cryptography.fernet import Fernet
import os
import argparse
from dotenv import load_dotenv, find_dotenv, set_key

ENCODING = 'utf-8'
FERNET_KEY = 'FERNET_KEY'

# find .env automagically by walking up directories until it's found
dotenv_path = find_dotenv()

# load up the entries as environment variables
load_dotenv(dotenv_path)

def generate_key(save = True):
    key = Fernet.generate_key()
    if save:
        set_key(dotenv_path, FERNET_KEY, key.decode(ENCODING))

    return key

def save_login(website_name: str, key: bytes, user: str, pw: str, save = True):
    fern = Fernet(key)

    user = fern.encrypt(user.encode()).decode(ENCODING)
    pw = fern.encrypt(pw.encode()).decode(ENCODING)
    if save:
        set_key(dotenv_path, USER_KEY, user)
        set_key(dotenv_path, PW_KEY, pw)

    return user, pw

def get_login(website_name: str, key: bytes, encrypted_user: str=None, encrypted_pw: str=None):
    fern = Fernet(key)

    if encrypted_user==None and encrypted_pw==None:
        encrypted_user = os.environ.get(USER_KEY)
        encrypted_pw = os.environ.get(PW_KEY)

    encrypted_user = encrypted_user.encode()
    encrypted_pw = encrypted_pw.encode()

    user = fern.decrypt(encrypted_user).decode(ENCODING)
    pw = fern.decrypt(encrypted_pw).decode(ENCODING)

    return user, pw


if __name__ == '__main__':
    func_list = [generate_key, save_login, get_login]
    func_names = [f.__name__ for f in func_list]
    funcs_dict = dict(zip(func_names, func_list))

    parser = argparse.ArgumentParser(description='account auth')
    # Add the -f/--func argument
    parser.add_argument('-f', '--func', dest='func',
                        choices=func_names,
                        required=True,
                        help="""Choose one of the specified function to be run.""")
    parser.add_argument('-ws', '--website-name', dest='website_name',
                        choices=['FIDELITY'],
                        required=False,
                        help="""Choose one of the specified function to be run.""")
    parser.add_argument('--user', dest='user',
                        required=False,
                        help="""Login username.""")
    parser.add_argument('--pw', dest='pw',
                        required=False,
                        help="""Login password.""")
    args = parser.parse_args()

    chosen_func = funcs_dict[args.func]
    SAVE = True
    if chosen_func.__name__ == 'generate_key':
        chosen_func(save = SAVE)
    else:
        key = os.environ.get(FERNET_KEY).encode()
        USER_KEY = f'{args.website_name}_USER'
        PW_KEY = f'{args.website_name}_PW'
        if chosen_func.__name__ == 'save_login':
            chosen_func(args.website_name, key, args.user, args.pw, save = SAVE)
        elif chosen_func.__name__ == 'get_login':
            user, pw = chosen_func(args.website_name, key)
            print(user, pw)
