from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
# Note: the connection string after :// contains the following info:
# user:password@server:portnumber/databaseName
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:beproductive@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean)

    def __init__(self, name):
        self.name = name
        self.completed = False

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.route('/login', methods=['POST', 'GET'])
def login():
    email= request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        # Todo - "remember" that the user has logged in
        return redirect('/')
    else:
        # Todo - explain why login failed
        return "<h1>Error!<h1>"
    
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    email = request.form['email']
    password = request.form['password']
    verify = request.form['verify']

    # Todo - validate user's data

    existing_user = User.query.filter_by(email=email).first()
    if not existing_user:
        new_user = User(new_user)
        db.session.add(new_user)
        db.session.commit()
        # Todo - "remember" the user
        return redirect('/')
    else:
        # Todo - user better response messaging
        return "<h1>Duplicate user</h1>"
    
    return render_template('register.html')

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        task_name = request.form['task']
        new_task = Task(task_name)
        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.filter_by(completed=False).all()
    completed_tasks = Task.query.filter_by(completed=True).all()
    
    return render_template('todos.html',title="Get It Done!", tasks=tasks, completed_tasks=completed_tasks)

@app.route('/delete-task', methods=['POST'])
def delete_task():

    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)
    db.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run()