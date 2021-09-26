from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from app import User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Todo.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.sno} - {self.title} - {self.desc}'


@app.route("/", methods=['GET', 'POST'])
def MyTodo():
    if request.method=='POST':
        title= request.form["title"]
        descripton= request.form["desc"]
        # print(title)
        todo = Todo(title=title, desc=descripton)
        db.session.add(todo)
        db.session.commit()


    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)
    # return "<p>Hello, World!</p>"


@app.route("/show")
def show():
    allTodo = Todo.query.all()
    print(allTodo)
    return "<p>This is me Arindam Bhowal</p>"



@app.route("/delete/<int:sno>")
def delete(sno):
    del_todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(del_todo)
    db.session.commit()
    return redirect("/")


@app.route("/update/<int:sno>", methods= ['GET','POST'])
def update(sno):
    if request.method=='POST':
        title= request.form['title']
        description= request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title= title
        todo.desc= description

        db.session.add(todo)
        db.session.commit()
        return redirect('/')


    updated_todo= Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=updated_todo)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
