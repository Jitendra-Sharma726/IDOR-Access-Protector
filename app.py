from flask import Flask, render_template, request, redirect, url_for, session, abort
import sqlite3

app = Flask(__name__)

# Never use a hardcoded secret key in production. This is just for development purposes.

app.secret_key= 'supersecret_dev_key'
DB_FILE = 'users.db'

def get_db_connection():
  return sqlite3.connect(DB_FILE)

@app.route('/')
def index():
  if 'user_id' in session:
    return redirect(url_for('dashboard'))
  return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
  error= None
  if request.method == 'POST':
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    user_record = cursor.fetchone()
    conn.close()

    if user_record and user_record[1] == password:
      session['user_id'] = user_record[0]
      session['username'] = username
      return redirect(url_for('dashboard'))
  else:
    error = "Invalid credentials"

return render_template('login.html', error=error)


@app.route('/dashboard')
def dashboard():
  if 'user_id' not in session:
    return redirect(url_for('login'))

conn = get_db_connection()
cursor = conn.cursor()
# safely fetch only the documents owned by the logged-in user
cursor.execute("SELECT doc_id, title FROM documents WHERE owner_id = ?", (session['user_id'],))
user_docs = cursor.fetchall()
conn.close

return render_template('dashboard.html', username=session['username'], docs=user_docs)


@app.route('/view')
def view_document():
  if 'user_id' not in session:
    return redirect(url_for('login'))

requested_doc_id = request.args.get('doc_id')
if not requested_doc_id:
  return "Missing doc_id parameter", 400

conn = get_db_connection()
cursor = conn.cursor()

# VULNERABILITY : Insecure Direct Object Reference (IDOR)
# The system blindly trusts the 'doc_id' provided in the URL without checking who actually owns it.
# An attacker can just chang the number in the URL to read anyone else's private files.

# TODO 1: Redesign this SQL query to act as an authorization firewall.
# TODO 2: Require TWO conditions to be true: the document must match the requested 'doc_id', AND the document's 'owner_id' must match the currently looged-in user's ID(stored in the Flask session).
# TODO 3: Update the parameter tuple(...) to safely pass both variable into your new query.

cursor.execute("SELECT title, content FROM documents WHERE doc_id = ?", (requested_doc_id,))

document_data = cursor.fetchone()
conn.close()

#if the document doesn't exist ( or the patched query blocks access), return an error 
if not document_data:
  abort(403, description="Access Denied or Document Not Found")
  
return render_template('document.html', title=document_data[0], content=document_data[1])


@app.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('login'))


if __name__  == '__main__':
  app.run(host = '0.0.0.0', port=3000, debug=True)





















































    
























