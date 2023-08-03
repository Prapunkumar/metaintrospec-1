# app.py

from flask import Flask, render_template, request,jsonify
import mysql.connector
import json
import os

app = Flask(__name__)
app.secret_key = "students_help"


# Database configuration
app.config['MYSQL_HOST'] = os.environ['MYSQL_HOST']
app.config['MYSQL_USER'] = os.environ['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = os.environ['MYSQL_DB']

# Load questions 
with open('questions.txt') as f:
  questions = f.readlines()
print(questions)
# Set up the database connection
def create_conn():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Priyakavya@8280",
        database="students"
    )

@app.route('/', methods=['GET', 'POST'])
def details():
    print(request.method)
    return render_template("details.html")

@app.route('/submit', methods=['POST'])
def submit_details():
    print(request.method)
    if request.method == 'POST':
        # Process form submission
        name = request.form['name']
        email = request.form['email']
        conn = create_conn()
        cursor = conn.cursor()

        query = "SELECT attempt_count FROM student_details WHERE email = %s"
        
        cursor.execute(query, (email,))
        attempt_count= cursor.fetchone()
        print(attempt_count)
        if attempt_count is None:
            # Insert the new record if the email is not present
            insert_query = "INSERT INTO student_details (name, email, attempt_count) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (name, email, 0))
            conn.commit()
            cursor.close()
            conn.close()
            return render_template('index.html', questions=questions[0:5],email=email,count=0)
        else:
            index=attempt_count[0]*5
            print(attempt_count[0])
            return render_template('index.html', questions=questions[index:index+5],email=email,count=attempt_count[0])
        
    return render_template('details.html')

# @app.route('/index', methods=['POST'])
# def index():
#     print("Helloworld")
#     if request.method == 'POST':
#         email = request.form.get('email')
#         print(email)
#         attempt_count= validate_user(email)
#         print(attempt_count)
#         answers = {f'answer{i}': request.form[f'answer{i}'] for i in range(attempt_count*5+1, attempt_count*5+6)}
#         answers_json = json.dumps(answers)
#         print(answers)
#         conn = create_conn()
#         cursor = conn.cursor()

#         query = "INSERT INTO student_eval (email, answers) VALUES (%s, %s)"
#         cursor.execute(query, ( email, answers_json))

#         conn.commit()

#         update_query = "UPDATE student_details SET attempt_count = attempt_count + 1 WHERE email = %s"
#         cursor.execute(update_query, (email,))
#         conn.commit()
#         cursor.close()
#         conn.close()
    
#         return jsonify({"status": "success", "message": "Answers submitted successfully"})

#     return render_template('index.html', questions=questions)


@app.route('/index', methods=['POST'])
def index():
    print("Helloworld")
    if request.method == 'POST':
        email = request.form.get('email')
        print(email)
        attempt_count= validate_user(email)
        print(attempt_count)
        answers = {f'answer{i}': request.form[f'answer{i}'] for i in range(attempt_count*5+1, attempt_count*5+6)}
        answers_json = json.dumps(answers)
        print(answers)
        for answer in answers.keys():
            print(answers[answer])
        conn = create_conn()
        cursor = conn.cursor()

        query = "INSERT INTO student_eval (email, answers) VALUES (%s, %s)"
        cursor.execute(query, ( email, answers_json))

        conn.commit()

        update_query = "UPDATE student_details SET attempt_count = attempt_count + 1 WHERE email = %s"
        cursor.execute(update_query, (email,))
        conn.commit()
        cursor.close()
        conn.close()
    
        return jsonify({"status": "success", "message": "Answers submitted successfully"})

    return render_template('index.html', questions=questions)


def validate_user(email):
    conn = create_conn()
    cursor = conn.cursor()
    query = "SELECT attempt_count FROM student_details WHERE email = %s"
    cursor.execute(query, (email,))
    attempt_count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return attempt_count

if __name__ == '__main__':
  app.run(debug=True)

