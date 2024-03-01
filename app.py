from flask import Flask, render_template, request, redirect, session, url_for
from flask_mysqldb import MySQL
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(24)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'quiz_db'

# Initialize MySQL
mysql = MySQL(app)

# Sample questions
questions = [
    {
        'id': 1,
        'question': 'What is the capital of France?',
        'options': ['Paris', 'London', 'Berlin', 'Madrid'],
        'correct_answer': 'Paris'
    },
    {
        'id': 2,
        'question': 'What is 2 + 2?',
        'options': ['3', '4', '5', '6'],
        'correct_answer': '4'
    }
]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        score = 0
        for question in questions:
            answer = request.form.get(str(question['id']))
            if answer == question['correct_answer']:
                score += 1
        # Save score to database
        if 'username' in session:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO scores (username, score) VALUES (%s, %s)", (session['username'], score))
            mysql.connection.commit()
            cur.close()
        return render_template('result.html', score=score)
    return render_template('quiz.html', questions=questions)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
       
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
