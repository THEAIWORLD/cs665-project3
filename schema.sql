DROP TABLE IF EXISTS loans;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS authors;
DROP TABLE IF EXISTS members;
DROP TABLE IF EXISTS categories;

CREATE TABLE categories (
    category_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT    NOT NULL UNIQUE,
    description   TEXT
);

CREATE TABLE authors (
    author_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name   TEXT    NOT NULL,
    last_name    TEXT    NOT NULL,
    nationality  TEXT
);

CREATE TABLE books (
    book_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    title        TEXT    NOT NULL,
    isbn         TEXT    NOT NULL UNIQUE,
    author_id    INTEGER NOT NULL,
    category_id  INTEGER NOT NULL,
    total_copies INTEGER NOT NULL DEFAULT 1,
    available_copies INTEGER NOT NULL DEFAULT 1,
    published_year INTEGER,
    FOREIGN KEY (author_id)   REFERENCES authors(author_id)   ON DELETE RESTRICT,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE RESTRICT,
    CHECK (total_copies >= 1),
    CHECK (available_copies >= 0),
    CHECK (available_copies <= total_copies)
);

CREATE TABLE members (
    member_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name   TEXT    NOT NULL,
    last_name    TEXT    NOT NULL,
    email        TEXT    NOT NULL UNIQUE,
    phone        TEXT,
    join_date    TEXT    NOT NULL DEFAULT (date('now'))
);

CREATE TABLE loans (
    loan_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id      INTEGER NOT NULL,
    member_id    INTEGER NOT NULL,
    loan_date    TEXT    NOT NULL DEFAULT (date('now')),
    due_date     TEXT    NOT NULL,
    return_date  TEXT,
    status       TEXT    NOT NULL DEFAULT 'active'
                         CHECK (status IN ('active','returned','overdue')),
    FOREIGN KEY (book_id)   REFERENCES books(book_id)   ON DELETE RESTRICT,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE RESTRICT
);

INSERT INTO categories (name, description) VALUES
    ('Fiction','Novels and fictional stories'),
    ('Non-Fiction','Factual books and essays'),
    ('Science','Books about natural sciences'),
    ('Technology','Programming and tech topics'),
    ('History','World and regional history');

INSERT INTO authors (first_name, last_name, nationality) VALUES
    ('George','Orwell','British'),
    ('J.K.','Rowling','British'),
    ('Frank','Herbert','American'),
    ('Walter','Isaacson','American'),
    ('Yuval','Harari','Israeli');

INSERT INTO books (title, isbn, author_id, category_id, total_copies, available_copies, published_year) VALUES
    ('1984','978-0451524935',1,1,3,3,1949),
    ('Animal Farm','978-0451526342',1,1,2,2,1945),
    ('Harry Potter and the Sorcerers Stone','978-0590353427',2,1,4,4,1997),
    ('Dune','978-0441013593',3,1,2,2,1965),
    ('Steve Jobs','978-1451648539',4,2,3,3,2011),
    ('Sapiens','978-0062316110',5,5,2,2,2011);

INSERT INTO members (first_name, last_name, email, phone, join_date) VALUES
    ('Alice','Johnson','alice@email.com','316-555-0101','2024-01-15'),
    ('Bob','Smith','bob@email.com','316-555-0102','2024-02-20'),
    ('Carol','White','carol@email.com','316-555-0103','2024-03-10'),
    ('David','Brown','david@email.com','316-555-0104','2024-04-05');