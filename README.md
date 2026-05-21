\# Library Management System

\### CS665 Project 3 - Full Stack Python Application



A full-stack web application for managing a library's books, members, and loans. Built with Python Flask, SQLite, and Bootstrap 5.



\---



\## What is this app?



This is a Library Management System that allows librarians to:

\- Add, edit, and delete books and authors

\- Register and manage library members

\- Checkout books to members and track return dates

\- View a live dashboard with library statistics



\---



\## Tech Stack



\- \*\*Backend:\*\* Python 3, Flask

\- \*\*Database:\*\* SQLite

\- \*\*ORM/Driver:\*\* sqlite3 (DB-API)

\- \*\*Frontend:\*\* HTML5, CSS3, Bootstrap 5, Jinja2

\- \*\*Version Control:\*\* Git



\---



\## Installation Instructions



\### Step 1 - Clone the repository### Step 2 - Create virtual environment

\### Step 3 - Install dependencies

\---



\## Database Setup



The database is created automatically on first run. To manually set it up:



\---



\## Usage



\### Run the application

Then open your browser and go to:

\---



\## Main Features



| Feature | Description |

|---|---|

| Dashboard | Shows total books, members, active loans, and category stats |

| Books | Add, edit, delete, and search books |

| Members | Register members and view their loan history |

| Loans | Checkout books and mark returns |

| Authors | Manage author records |

| Transactions | Checkout and return use SQL transactions |

| Validation | Server-side validation on all forms |



\---



\## Project Structure



cs665-project3/

├── app.py               # Main Flask application

├── schema.sql           # Database schema and seed data

├── requirements.txt     # Python dependencies

├── README.md            # This file

├── NORMALIZATION.md     # 3NF normalization report

├── static/

│   └── css/

│       └── style.css    # Custom styles

└── templates/

├── base.html        # Base layout

├── dashboard.html   # Dashboard page

├── books.html       # Books CRUD

├── members.html     # Members CRUD

├── loans.html       # Loans management

├── authors.html     # Authors management

└── member\_detail.html  # Member loan history





