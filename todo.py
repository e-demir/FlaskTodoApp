from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/emrullah.demir/Desktop/py4e/FlaskTodo/todo.db'
db = SQLAlchemy(app)


@app.route("/")
def Index():
    todos = Todo.query.all()
    count = len(todos)
    return render_template("index.html", todos=todos, count=count)


@app.route("/delete/<string:id>")
def Delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("Index"))


@app.route("/detail/<string:id>")
def Detail(id):
    todo = Todo.query.filter_by(id=id).first()
    return render_template("detail.html", todo = todo)

@app.route("/mainpage")
def MainPage():
     return redirect(url_for("Index"))

@app.route("/complete/<string:id>")
def Complete(id):
    todo =  Todo.query.filter_by(id=id).first()
    if todo is not None:
        if todo.complete == False:
            todo.complete = True
        else:
            todo.complete = False

    db.session.commit()
    return redirect(url_for("Index"))

@app.route("/add", methods=["GET","POST"])
def Add():
    title = request.form.get("title")
    content = request.form.get("content")
    todo = Todo(title = title, content = content, complete = False)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for("Index"))
    

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    content = db.Column(db.Text)
    complete = db.Column(db.Boolean)

if __name__ == "__main__":
    app.run(debug=True)