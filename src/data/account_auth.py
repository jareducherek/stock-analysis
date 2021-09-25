from cryptography.fernet import Fernet
import os
import argparse

def generate_key(folder):
    key = Fernet.generate_key()

    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, 'fernet_key.txt')
    #os.remove(file_path)
    f = open(file_path, 'wb+')
    f.write(key)


def save_login(folder, user: str, pw: str):
    file_path = os.path.join(folder, 'fernet_key.txt')
    f = open(file_path, 'rb')
    key = f.readline()
    fern = Fernet(key)

    file_path = os.path.join(folder, 'account.txt')
    user = fern.encrypt(bytes(user, 'utf-8')) + b'\n'
    pw = fern.encrypt(bytes(pw, 'utf-8')) + b'\n'
    f = open(file_path, 'wb+')
    f.writelines([user, pw])


def get_login(folder):
    file_path = os.path.join(folder, 'fernet_key.txt')
    f = open(file_path, 'rb')
    key = f.readline()
    fern = Fernet(key)

    file_path = os.path.join(folder, 'account.txt')
    f = open(file_path, 'rb')
    user, pw = f.readlines()
    user = fern.decrypt(user)
    pw = fern.decrypt(pw)

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
    # Add the -p/--path argument: required path to authentication folder
    parser.add_argument('-p', '--path', dest='path',
                        required=True,
                        help="""Indicate the path where the files are saved.""")
    parser.add_argument('--user', dest='user',
                        required=False,
                        help="""Login username.""")
    parser.add_argument('--pw', dest='pw',
                        required=False,
                        help="""Login password.""")
    args = parser.parse_args()

    chosen_func = funcs_dict[args.func]
    if chosen_func.__name__ == 'generate_key':
        chosen_func(args.path)
    if chosen_func.__name__ == 'save_login':
        chosen_func(args.path, args.user, args.pw)
    if chosen_func.__name__ == 'get_login':
        user, pw = chosen_func(args.path)
        print(user, pw)
