from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('visitor.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    visitors = conn.execute('SELECT * FROM visitor').fetchall()
    conn.close()
    return render_template('index.html', visitors=visitors)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        name = request.form['name']
        purpose = request.form['purpose']
        contact = request.form['contact']

        conn = get_db_connection()
        conn.execute('INSERT INTO visitor (name, purpose, contact) VALUES (?, ?, ?)',
                     (name, purpose, contact))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM visitor WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
