import sqlite3
import os
from datetime import date, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, g

app = Flask(__name__)
app.secret_key = "cs665_library_secret_key"
DATABASE = "library.db"

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys = ON")
    return db

@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def init_db():
    if not os.path.exists(DATABASE):
        with app.app_context():
            db = get_db()
            with open("schema.sql", "r") as f:
                db.executescript(f.read())
            db.commit()

@app.route("/")
def dashboard():
    db = get_db()
    stats = db.execute("""
        SELECT
            (SELECT COUNT(*) FROM books) AS total_books,
            (SELECT COUNT(*) FROM members) AS total_members,
            (SELECT COUNT(*) FROM loans WHERE status='active') AS active_loans,
            (SELECT COUNT(*) FROM loans WHERE status='overdue') AS overdue_loans,
            (SELECT SUM(available_copies) FROM books) AS total_available,
            (SELECT AVG(total_copies) FROM books) AS avg_copies
    """).fetchone()
    category_stats = db.execute("""
        SELECT c.name, COUNT(b.book_id) AS book_count, SUM(b.available_copies) AS available
        FROM categories c LEFT JOIN books b ON c.category_id = b.category_id
        GROUP BY c.category_id ORDER BY book_count DESC
    """).fetchall()
    recent_loans = db.execute("""
        SELECT l.loan_id, m.first_name || ' ' || m.last_name AS member_name,
               b.title, l.loan_date, l.due_date, l.status
        FROM loans l JOIN members m ON l.member_id=m.member_id
        JOIN books b ON l.book_id=b.book_id ORDER BY l.loan_id DESC LIMIT 5
    """).fetchall()
    return render_template("dashboard.html", stats=stats,
                           category_stats=category_stats, recent_loans=recent_loans)

@app.route("/books")
def books():
    db = get_db()
    search = request.args.get("search", "").strip()
    if search:
        rows = db.execute("""
            SELECT b.book_id, b.title, b.isbn, b.published_year,
                   b.total_copies, b.available_copies,
                   a.first_name || ' ' || a.last_name AS author_name, c.name AS category_name
            FROM books b JOIN authors a ON b.author_id=a.author_id
            JOIN categories c ON b.category_id=c.category_id
            WHERE b.title LIKE ? OR a.last_name LIKE ? OR b.isbn LIKE ?
            ORDER BY b.title
        """, (f"%{search}%", f"%{search}%", f"%{search}%")).fetchall()
    else:
        rows = db.execute("""
            SELECT b.book_id, b.title, b.isbn, b.published_year,
                   b.total_copies, b.available_copies,
                   a.first_name || ' ' || a.last_name AS author_name, c.name AS category_name
            FROM books b JOIN authors a ON b.author_id=a.author_id
            JOIN categories c ON b.category_id=c.category_id ORDER BY b.title
        """).fetchall()
    authors = db.execute("SELECT * FROM authors ORDER BY last_name").fetchall()
    categories = db.execute("SELECT * FROM categories ORDER BY name").fetchall()
    return render_template("books.html", books=rows, authors=authors,
                           categories=categories, search=search)

@app.route("/books/add", methods=["POST"])
def add_book():
    title = request.form.get("title","").strip()
    isbn = request.form.get("isbn","").strip()
    author_id = request.form.get("author_id","").strip()
    category_id = request.form.get("category_id","").strip()
    total_copies = request.form.get("total_copies","1").strip()
    pub_year = request.form.get("published_year","").strip()
    errors = []
    if not title: errors.append("Title is required.")
    if not isbn: errors.append("ISBN is required.")
    if not author_id: errors.append("Author is required.")
    if not category_id: errors.append("Category is required.")
    if not total_copies.isdigit() or int(total_copies) < 1:
        errors.append("Total copies must be a positive integer.")
    if pub_year and (not pub_year.isdigit() or not (1000 <= int(pub_year) <= date.today().year)):
        errors.append("Published year must be a valid year.")
    if errors:
        for e in errors: flash(e, "danger")
        return redirect(url_for("books"))
    db = get_db()
    try:
        db.execute("""INSERT INTO books (title,isbn,author_id,category_id,total_copies,available_copies,published_year)
                      VALUES (?,?,?,?,?,?,?)""",
                   (title,isbn,author_id,category_id,int(total_copies),int(total_copies),
                    int(pub_year) if pub_year else None))
        db.commit()
        flash(f'Book "{title}" added!', "success")
    except sqlite3.IntegrityError:
        flash("A book with that ISBN already exists.", "danger")
    return redirect(url_for("books"))

@app.route("/books/edit/<int:book_id>", methods=["POST"])
def edit_book(book_id):
    title = request.form.get("title","").strip()
    isbn = request.form.get("isbn","").strip()
    author_id = request.form.get("author_id","").strip()
    category_id = request.form.get("category_id","").strip()
    total_copies = request.form.get("total_copies","1").strip()
    pub_year = request.form.get("published_year","").strip()
    if not title or not isbn:
        flash("Title and ISBN are required.", "danger")
        return redirect(url_for("books"))
    db = get_db()
    db.execute("UPDATE books SET title=?,isbn=?,author_id=?,category_id=?,total_copies=?,published_year=? WHERE book_id=?",
               (title,isbn,author_id,category_id,int(total_copies),int(pub_year) if pub_year else None,book_id))
    db.commit()
    flash("Book updated!", "success")
    return redirect(url_for("books"))

@app.route("/books/delete/<int:book_id>", methods=["POST"])
def delete_book(book_id):
    db = get_db()
    active = db.execute("SELECT COUNT(*) FROM loans WHERE book_id=? AND status='active'",(book_id,)).fetchone()[0]
    if active > 0:
        flash("Cannot delete a book with active loans.", "danger")
        return redirect(url_for("books"))
    book = db.execute("SELECT title FROM books WHERE book_id=?",(book_id,)).fetchone()
    db.execute("DELETE FROM books WHERE book_id=?",(book_id,))
    db.commit()
    flash(f'Book "{book["title"]}" deleted.', "success")
    return redirect(url_for("books"))

@app.route("/members")
def members():
    db = get_db()
    rows = db.execute("""
        SELECT m.*, COUNT(l.loan_id) AS total_loans,
               SUM(CASE WHEN l.status='active' THEN 1 ELSE 0 END) AS active_loans
        FROM members m LEFT JOIN loans l ON m.member_id=l.member_id
        GROUP BY m.member_id ORDER BY m.last_name
    """).fetchall()
    return render_template("members.html", members=rows)

@app.route("/members/add", methods=["POST"])
def add_member():
    first = request.form.get("first_name","").strip()
    last = request.form.get("last_name","").strip()
    email = request.form.get("email","").strip()
    phone = request.form.get("phone","").strip()
    if not first or not last:
        flash("First and last name are required.", "danger")
        return redirect(url_for("members"))
    if not email or "@" not in email:
        flash("A valid email is required.", "danger")
        return redirect(url_for("members"))
    db = get_db()
    try:
        db.execute("INSERT INTO members (first_name,last_name,email,phone) VALUES (?,?,?,?)",
                   (first,last,email,phone or None))
        db.commit()
        flash(f"Member {first} {last} added!", "success")
    except sqlite3.IntegrityError:
        flash("Email already exists.", "danger")
    return redirect(url_for("members"))

@app.route("/members/edit/<int:member_id>", methods=["POST"])
def edit_member(member_id):
    first = request.form.get("first_name","").strip()
    last = request.form.get("last_name","").strip()
    email = request.form.get("email","").strip()
    phone = request.form.get("phone","").strip()
    if not first or not last or not email or "@" not in email:
        flash("All fields required with valid email.", "danger")
        return redirect(url_for("members"))
    db = get_db()
    db.execute("UPDATE members SET first_name=?,last_name=?,email=?,phone=? WHERE member_id=?",
               (first,last,email,phone or None,member_id))
    db.commit()
    flash("Member updated!", "success")
    return redirect(url_for("members"))

@app.route("/members/delete/<int:member_id>", methods=["POST"])
def delete_member(member_id):
    db = get_db()
    active = db.execute("SELECT COUNT(*) FROM loans WHERE member_id=? AND status='active'",(member_id,)).fetchone()[0]
    if active > 0:
        flash("Cannot delete a member with active loans.", "danger")
        return redirect(url_for("members"))
    mem = db.execute("SELECT first_name,last_name FROM members WHERE member_id=?",(member_id,)).fetchone()
    db.execute("DELETE FROM members WHERE member_id=?",(member_id,))
    db.commit()
    flash(f'Member {mem["first_name"]} {mem["last_name"]} deleted.', "success")
    return redirect(url_for("members"))

@app.route("/members/<int:member_id>")
def member_detail(member_id):
    db = get_db()
    member = db.execute("SELECT * FROM members WHERE member_id=?",(member_id,)).fetchone()
    if not member:
        flash("Member not found.", "danger")
        return redirect(url_for("members"))
    loan_history = db.execute("""
        SELECT l.loan_id, b.title, l.loan_date, l.due_date, l.return_date, l.status
        FROM loans l JOIN books b ON l.book_id=b.book_id
        WHERE l.member_id=? ORDER BY l.loan_id DESC
    """,(member_id,)).fetchall()
    return render_template("member_detail.html", member=member, loans=loan_history)

@app.route("/loans")
def loans():
    db = get_db()
    rows = db.execute("""
        SELECT l.loan_id, l.loan_date, l.due_date, l.return_date, l.status,
               m.first_name || ' ' || m.last_name AS member_name,
               b.title AS book_title, m.member_id, b.book_id
        FROM loans l JOIN members m ON l.member_id=m.member_id
        JOIN books b ON l.book_id=b.book_id ORDER BY l.loan_id DESC
    """).fetchall()
    books_avail = db.execute("SELECT book_id,title,available_copies FROM books WHERE available_copies>0 ORDER BY title").fetchall()
    members_list = db.execute("SELECT member_id, first_name || ' ' || last_name AS full_name FROM members ORDER BY last_name").fetchall()
    return render_template("loans.html", loans=rows, books=books_avail, members=members_list)

@app.route("/loans/checkout", methods=["POST"])
def checkout():
    book_id = request.form.get("book_id","").strip()
    member_id = request.form.get("member_id","").strip()
    days = request.form.get("loan_days","14").strip()
    if not book_id or not member_id:
        flash("Please select a book and member.", "danger")
        return redirect(url_for("loans"))
    if not days.isdigit() or not (1 <= int(days) <= 90):
        flash("Loan period must be 1-90 days.", "danger")
        return redirect(url_for("loans"))
    db = get_db()
    book = db.execute("SELECT title,available_copies FROM books WHERE book_id=?",(book_id,)).fetchone()
    if not book or book["available_copies"] < 1:
        flash("No copies available.", "danger")
        return redirect(url_for("loans"))
    loan_date = date.today().isoformat()
    due_date = (date.today() + timedelta(days=int(days))).isoformat()
    try:
        db.execute("BEGIN")
        db.execute("INSERT INTO loans (book_id,member_id,loan_date,due_date) VALUES (?,?,?,?)",
                   (book_id,member_id,loan_date,due_date))
        db.execute("UPDATE books SET available_copies=available_copies-1 WHERE book_id=?",(book_id,))
        db.execute("COMMIT")
        flash(f'"{book["title"]}" checked out! Due: {due_date}', "success")
    except Exception as ex:
        db.execute("ROLLBACK")
        flash(f"Checkout failed: {ex}", "danger")
    return redirect(url_for("loans"))

@app.route("/loans/return/<int:loan_id>", methods=["POST"])
def return_book(loan_id):
    db = get_db()
    loan = db.execute("SELECT l.book_id, b.title FROM loans l JOIN books b ON l.book_id=b.book_id WHERE l.loan_id=?",(loan_id,)).fetchone()
    if not loan:
        flash("Loan not found.", "danger")
        return redirect(url_for("loans"))
    today = date.today().isoformat()
    try:
        db.execute("BEGIN")
        db.execute("UPDATE loans SET status='returned',return_date=? WHERE loan_id=?",(today,loan_id))
        db.execute("UPDATE books SET available_copies=available_copies+1 WHERE book_id=?",(loan["book_id"],))
        db.execute("COMMIT")
        flash(f'"{loan["title"]}" returned!', "success")
    except Exception as ex:
        db.execute("ROLLBACK")
        flash(f"Return failed: {ex}", "danger")
    return redirect(url_for("loans"))

@app.route("/authors")
def authors():
    db = get_db()
    rows = db.execute("""
        SELECT a.*, COUNT(b.book_id) AS book_count
        FROM authors a LEFT JOIN books b ON a.author_id=b.author_id
        GROUP BY a.author_id ORDER BY a.last_name
    """).fetchall()
    return render_template("authors.html", authors=rows)

@app.route("/authors/add", methods=["POST"])
def add_author():
    first = request.form.get("first_name","").strip()
    last = request.form.get("last_name","").strip()
    nat = request.form.get("nationality","").strip()
    if not first or not last:
        flash("First and last name are required.", "danger")
        return redirect(url_for("authors"))
    db = get_db()
    db.execute("INSERT INTO authors (first_name,last_name,nationality) VALUES (?,?,?)",(first,last,nat or None))
    db.commit()
    flash(f"Author {first} {last} added!", "success")
    return redirect(url_for("authors"))

@app.route("/authors/delete/<int:author_id>", methods=["POST"])
def delete_author(author_id):
    db = get_db()
    count = db.execute("SELECT COUNT(*) FROM books WHERE author_id=?",(author_id,)).fetchone()[0]
    if count > 0:
        flash("Cannot delete an author who has books.", "danger")
        return redirect(url_for("authors"))
    author = db.execute("SELECT first_name,last_name FROM authors WHERE author_id=?",(author_id,)).fetchone()
    db.execute("DELETE FROM authors WHERE author_id=?",(author_id,))
    db.commit()
    flash(f'Author {author["first_name"]} {author["last_name"]} deleted.', "success")
    return redirect(url_for("authors"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)