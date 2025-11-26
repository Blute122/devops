from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
# Database config (Creates a local file database)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Database Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    course = db.Column(db.String(100), nullable=False)
    percentage = db.Column(db.Float, nullable=False)

# Create DB tables if they don't exist
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/apply', methods=['POST'])
def apply():
    name = request.form['name']
    email = request.form['email']
    course = request.form['course']
    percentage = request.form['percentage']
    
    new_student = Student(name=name, email=email, course=course, percentage=percentage)
    try:
        db.session.add(new_student)
        db.session.commit()
        return render_template('index.html', message="Application Submitted Successfully!")
    except:
        return render_template('index.html', message="Error: Email already exists!")

@app.route('/admin')
def admin():
    students = Student.query.all()
    return render_template('dashboard.html', students=students)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

