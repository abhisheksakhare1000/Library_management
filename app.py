from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Connect to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    database='library_management'
)

cursor = conn.cursor(dictionary=True)

# Create tables if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        bookID INT PRIMARY KEY,
        title VARCHAR(255),
        author VARCHAR(255)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS issued_books (
        bookID INT,
        memberName VARCHAR(255),
        returnDate DATE,
        FOREIGN KEY (bookID) REFERENCES books(bookID)
    )
""")

# Routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        bookID = request.form['bookID']
        title = request.form['title']
        author = request.form['author']

        cursor.execute("INSERT INTO books (bookID, title, author) VALUES (%s, %s, %s)", (bookID, title, author))
        conn.commit()

        return redirect('/list_books')

    return render_template('add_book.html')

@app.route('/issue_book', methods=['GET', 'POST'])
def issue_book():
    if request.method == 'POST':
        bookID = request.form['bookID']
        memberName = request.form['memberName']
        returnDate = request.form['returnDate']

        cursor.execute("INSERT INTO issued_books (bookID, memberName, returnDate) VALUES (%s, %s, %s)", (bookID, memberName, returnDate))
        conn.commit()

        return redirect('/list_issued_books')

    return render_template('issue_book.html')

@app.route('/return_book', methods=['GET', 'POST'])
def return_book():
    if request.method == 'POST':
        bookID = request.form['bookID']
        memberName = request.form['memberName']

        cursor.execute("DELETE FROM issued_books WHERE bookID = %s AND memberName = %s", (bookID, memberName))
        conn.commit()

        return redirect('/list_issued_books')

    return render_template('return_book.html')

@app.route('/list_books')
def list_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    return render_template('list_books.html', books=books)

@app.route('/list_issued_books')
def list_issued_books():
    cursor.execute("SELECT * FROM issued_books")
    issued_books = cursor.fetchall()
    return render_template('list_issued_books.html', issued_books=issued_books)

if __name__ == '__main__':
    app.run(debug=True)
