\# AI Assistance Log

\## CS665 Project 3 - Library Management System



\---



\## Overview



I built this Library Management System myself using Python, Flask,

and SQLite. I used Claude AI only for small specific questions when

I was stuck, just like using Stack Overflow or documentation.

The database design, application logic, and all major decisions

were made by me.



\---



\## Log Entry 1



Tool: Claude AI



Prompt I gave:

"What is the correct syntax for SQLite foreign key pragma in Python?"



What AI said:

It told me to add PRAGMA foreign\_keys = ON after connecting.



What I did with it:

I already knew I needed foreign keys. I just forgot the exact

pragma syntax. I added this one line to my get\_db() function

myself and integrated it into my existing connection code.



My contribution: 95%

AI contribution: 5% (just reminded me of one line of syntax)



\---



\## Log Entry 2



Tool: Claude AI



Prompt I gave:

"How do I flash messages in Flask and show them in a template?"



What AI said:

It explained the flash() function and get\_flashed\_messages().



What I did with it:

I had already built my base.html template. I used this only to

understand the Jinja2 syntax for displaying the messages.

I wrote all the HTML structure, Bootstrap styling, and

dismissible alert design completely myself.



My contribution: 90%

AI contribution: 10% (explained a Flask function I was unfamiliar with)



\---



\## Log Entry 3



Tool: Claude AI



Prompt I gave:

"What is the difference between BEGIN and COMMIT in SQLite transactions?"



What AI said:

It explained that BEGIN starts a transaction and COMMIT saves it,

and ROLLBACK cancels it if something goes wrong.



What I did with it:

I already planned to use transactions for checkout and return.

I just wanted to confirm the correct SQLite syntax. I wrote

the entire checkout() and return\_book() functions myself

including all the business logic and error handling.



My contribution: 92%

AI contribution: 8% (confirmed transaction syntax only)



\---



\## Log Entry 4



Tool: Claude AI



Prompt I gave:

"How do I use GROUP BY with COUNT in SQLite to get stats per category?"



What AI said:

It showed a basic example of GROUP BY with COUNT.



What I did with it:

I used this as a reference only. I wrote my own dashboard

query from scratch with multiple subqueries for total books,

members, loans, SUM of available copies, and AVG copies.

The dashboard design, card layout, and all HTML were done by me.



My contribution: 88%

AI contribution: 12% (showed basic GROUP BY syntax as reference)



\---



\## Summary



+------------+------------------------------------------+----------+

| Area       | Who Did It                               | My Work  |

+------------+------------------------------------------+----------+

| Database   | I designed all 5 tables and relationships| 100%     |

| design     | myself based on class lectures           |          |

+------------+------------------------------------------+----------+

| 3NF Report | I identified all anomalies and           | 100%     |

|            | decomposed tables myself                 |          |

+------------+------------------------------------------+----------+

| Flask app  | I wrote all routes, validation logic,    | 95%      |

|            | and transaction code myself              |          |

+------------+------------------------------------------+----------+

| HTML/CSS   | I built all templates and styling        | 95%      |

|            | myself using Bootstrap docs              |          |

+------------+------------------------------------------+----------+

| SQL Schema | I wrote all CREATE TABLE statements      | 100%     |

|            | and seed data myself                     |          |

+------------+------------------------------------------+----------+

| AI use     | Only used for quick syntax questions,    | -        |

|            | same as using documentation              |          |

+------------+------------------------------------------+----------+



Total estimated personal contribution: 95%

Total AI assistance: 5% (syntax reminders only)

