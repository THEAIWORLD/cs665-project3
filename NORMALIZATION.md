\# Normalization Report

\## CS665 Project 3 - Library Management System



\---



\## 1. Where We Started



Imagine all library data crammed into ONE big spreadsheet like this:



record\_id | book\_title | isbn | author\_first | author\_last | author\_nationality | category\_name | category\_description | member\_first | member\_last | member\_email | member\_phone | loan\_date | due\_date | return\_date | status | total\_copies | available\_copies



Every time someone borrowed a book, a new row was added with ALL

of this information repeated. This causes serious problems.



\---



\## 2. Problems Found (Anomalies)



+------------------+--------------------------------------------------+

| Problem Type     | What Goes Wrong                                  |

+------------------+--------------------------------------------------+

| Update Anomaly   | George Orwell's nationality is stored in 50      |

|                  | rows. Change one, the others stay wrong.         |

+------------------+--------------------------------------------------+

| Insert Anomaly   | Cannot add a new author to the system unless     |

|                  | they already have a book AND a loan record.      |

+------------------+--------------------------------------------------+

| Delete Anomaly   | Delete the last loan of a member and you lose    |

|                  | their name, email, and phone forever.            |

+------------------+--------------------------------------------------+



\---



\## 3. Step-by-Step Fix (1NF to 3NF)



STEP 1 - First Normal Form (1NF)

\---------------------------------

Rule: No repeating groups. Every cell has one value.

Result: The original table already satisfies 1NF.

Status: PASS





STEP 2 - Second Normal Form (2NF)

\-----------------------------------

Rule: Every column must depend on the WHOLE primary key,

&#x20;     not just part of it.



Problem found:

&#x20; author\_nationality depends only on author\_name,

&#x20; NOT on the full record\_id.



&#x20; isbn → book\_title (fine)

&#x20; isbn → author\_nationality (VIOLATION - author info

&#x20;        does not depend on the loan record)



Fix applied:

&#x20; Pulled authors out into their own separate table.

&#x20; Now author\_nationality lives with the author, not the loan.



Status: FIXED





STEP 3 - Third Normal Form (3NF)

\----------------------------------

Rule: No column should depend on another non-key column.

&#x20;     (No transitive dependencies)



Problems found:



&#x20; +-------------------------+----------------------------------+

&#x20; | Transitive Dependency   | Why It Is a Problem              |

&#x20; +-------------------------+----------------------------------+

&#x20; | category\_name           | category\_description tells us    |

&#x20; | → category\_description  | about the category, not the book |

&#x20; +-------------------------+----------------------------------+

&#x20; | member\_email            | member details belong to the     |

&#x20; | → member\_first/last     | person, not the loan record      |

&#x20; +-------------------------+----------------------------------+

&#x20; | author\_first/last       | nationality belongs to the       |

&#x20; | → author\_nationality    | author, not the book             |

&#x20; +-------------------------+----------------------------------+



Fix applied:

&#x20; Split into 5 clean tables:

&#x20; categories, authors, books, members, loans



Status: FIXED - Schema is now in 3NF





\---



\## 4. Final Schema After Normalization



TABLE: categories

+------------------+---------+------------------------+

| Column           | Type    | Rule                   |

+------------------+---------+------------------------+

| category\_id      | INTEGER | Primary Key            |

| name             | TEXT    | Required, Unique       |

| description      | TEXT    | Optional               |

+------------------+---------+------------------------+





TABLE: authors

+------------------+---------+------------------------+

| Column           | Type    | Rule                   |

+------------------+---------+------------------------+

| author\_id        | INTEGER | Primary Key            |

| first\_name       | TEXT    | Required               |

| last\_name        | TEXT    | Required               |

| nationality      | TEXT    | Optional               |

+------------------+---------+------------------------+





TABLE: books

+------------------+---------+------------------------+

| Column           | Type    | Rule                   |

+------------------+---------+------------------------+

| book\_id          | INTEGER | Primary Key            |

| title            | TEXT    | Required               |

| isbn             | TEXT    | Required, Unique       |

| author\_id        | INTEGER | Foreign Key → authors  |

| category\_id      | INTEGER | Foreign Key → categori |

| total\_copies     | INTEGER | Required, Min 1        |

| available\_copies | INTEGER | Required, Min 0        |

| published\_year   | INTEGER | Optional               |

+------------------+---------+------------------------+





TABLE: members

+------------------+---------+------------------------+

| Column           | Type    | Rule                   |

+------------------+---------+------------------------+

| member\_id        | INTEGER | Primary Key            |

| first\_name       | TEXT    | Required               |

| last\_name        | TEXT    | Required               |

| email            | TEXT    | Required, Unique       |

| phone            | TEXT    | Optional               |

| join\_date        | TEXT    | Required               |

+------------------+---------+------------------------+





TABLE: loans

+------------------+---------+------------------------+

| Column           | Type    | Rule                   |

+------------------+---------+------------------------+

| loan\_id          | INTEGER | Primary Key            |

| book\_id          | INTEGER | Foreign Key → books    |

| member\_id        | INTEGER | Foreign Key → members  |

| loan\_date        | TEXT    | Required               |

| due\_date         | TEXT    | Required               |

| return\_date      | TEXT    | Optional               |

| status           | TEXT    | active/returned/overdue|

+------------------+---------+------------------------+





\---



\## 5. Table Relationships (Plain English)



+----------------+----------+----------------+---------------------------+

| From Table     | Relation | To Table       | Meaning                   |

+----------------+----------+----------------+---------------------------+

| authors        | 1 to Many| books          | One author writes many    |

|                |          |                | books                     |

+----------------+----------+----------------+---------------------------+

| categories     | 1 to Many| books          | One category has many     |

|                |          |                | books                     |

+----------------+----------+----------------+---------------------------+

| members        | 1 to Many| loans          | One member borrows many   |

|                |          |                | books over time           |

+----------------+----------+----------------+---------------------------+

| books          | 1 to Many| loans          | One book has many loan    |

|                |          |                | records over time         |

+----------------+----------+----------------+---------------------------+





\---



\## 6. Summary



Before normalization: 1 bloated table with repeated data everywhere.

After normalization : 5 clean tables, each storing one thing only.



All update, insert, and delete anomalies have been eliminated.

The database is fully in Third Normal Form (3NF).

