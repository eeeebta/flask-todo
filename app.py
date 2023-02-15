from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# App configuration is not a concept we really talked about, but being able to
# set these session variables/app variables is still a pretty important concept
# to access data, or to set up the app to run in a certain way

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Creating a model is a concept that isn't necesarily unique to Flask, but it's
# an important concept for much of the web development world.
# A model is a class that represents a table in our database.

# This is also a class, so it represents both? Or maybe a model is just a class
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Todo %r>' % self.id


# Routing per app route is also a concept we touched upon
@app.route('/')
def home():
    todo_list = Todo.query.all()
    return render_template('index.html', todo_list=todo_list)


# Methods/[post/get] is also a concept I think we looked at
@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    new_todo = Todo(title=title)
    db.session.add(new_todo)
    db.session.commit()
    return redirect('/')


# Here there's also an argument being passed into the route
# which I think be something adjacent to props, or just regular
# being variables per each route

# This would also technically be reactive (applies to the
# other parts of this program) because these values are updated
# on the page, but not in real time (only after a reload)
@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.completed = not todo.completed
    db.session.commit()
    return redirect('/')


@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)
