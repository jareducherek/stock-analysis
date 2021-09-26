import pytest
from src.utils.account_auth import generate_key, save_login, get_login

def test_account_auth():
    key = generate_key(save=False)
    test_ws = 'test'
    test_user = 'test@email.com'
    test_pw = 'test_pw_123'

    enc_user, enc_pw = save_login(website_name='test', user=test_user, pw=test_pw, key=key, save=False)
    out_user, out_pw = get_login(website_name=test_ws, key=key, encrypted_user=enc_user, encrypted_pw=enc_pw)

    assert test_user == out_user
    assert test_pw == out_pw

