import requests
import hashlib
import sys

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, try again')
    return res

def get_password_leaks(hashes, to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for key, value in hashes:
        if key == to_check:
            return value


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5)

    return get_password_leaks(response, tail)

def main(args):
    for password in args:
        count = pwned_api_check(str(password))
        if count:
            print(f'{password} was found {count} times... maybe change it?')
        else:
            print(f'{password} was not found. Congrats!')

    while True:
        password = input('Enter your password (! to exit): ')
        if password == '!': break

        count = pwned_api_check(str(password))
        if count: 
            print(f'{password} was found {count} times... maybe change it?')
        else:
            print(f'{password} was not found. Congrats!')
    
    print('See ya')
main(sys.argv[1:])