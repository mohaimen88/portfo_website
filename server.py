from flask import Flask, render_template, url_for, request, redirect
import csv
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
print(__name__)


@app.route("/")
def my_home():
    return render_template('./index.html')

@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)

def write_to_file(data):
    with open('database.txt', mode='a') as file:
        email = data['email']
        subject = data['subject']
        message = data['message']
        file = file.write(f'\n{email},{subject},{message}')

def write_to_csv(data):
    with open('database.csv', newline='', mode='a') as csv_file:
        email = data['email']
        subject = data['subject']
        message = data['message']
        csv_writer = csv.writer(csv_file, delimiter=',',  quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])

#DATABASE SQLITE
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection




def execute_query(connection, query, email, subject, message):
    cursor = connection.cursor()
    try:
        cursor.execute(query, (email, subject, message))
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        connection = create_connection("sm_app.sqlite")
        data = request.form.to_dict()
        write_to_file(data)
        write_to_csv(data)
        
        email = data['email']
        subject = data['subject']
        message = data['message']
        new_message = '''
        INSERT INTO 
            messages (email, subject, message)
        VALUES
            (?, ?, ?)
        '''
        execute_query(connection, new_message, email, subject, message)

        return redirect('/thankyou.html')
    else:
        return 'something went wrong'


#Create the table
create_messages_table = """
CREATE TABLE IF NOT EXISTS messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT NOT NULL,
  subject TEXT NOT NULL,
  message TEXT NOT NULL

);
"""
# execure the create table query 
# execute_query(connection, create_messages_table) 

new_message = '''
INSERT INTO 
    messages (email, subject, message)
VALUES
    ('m@m.com', 'static test', 'static msg test')
'''
# execute_query(connection, new_message)





# @app.route("/work.html")
# def work():
#     return render_template('./work.html')

# @app.route("/about.html")
# def about():
#     return render_template('./about.html')

# @app.route("/contact.html")
# def contact():
#     return render_template('./contact.html')

# @app.route("/components.html")
# def components():
#     return render_template('./components.html')    