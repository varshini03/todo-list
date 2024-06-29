from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost:3306/todo_db"
db = SQLAlchemy(app)

# create class template for table
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}, {self.content}, {self.date_created}>'

@app.route('/', methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['task']
        taskObj = Todo(content = task_content)
        
        try:
            db.session.add(taskObj)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an exception while trying to add task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('page1.html', task=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task = Todo.query.get_or_404(id)

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an exception deleting the record"

@app.route('/update/<int:id>', methods = ['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error updating the record"

    if request.method == 'GET':
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)