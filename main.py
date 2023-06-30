from flask import Flask, render_template, request, flash, g
import os
import sqlite3
from todoDB import todoDB

DATABASE = '/tmp/todos_db.db'
DEBUG = True
SECRET_KEY = "dsfsldfjmsjkfnjrengern34"

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'todos_db.db')))

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

@app.route('/')
def index():
    db = get_db()
    dbase = todoDB(db)
    return render_template('index.html', todos = dbase.getTodos())

@app.route('/add', methods=['POST', 'GET'])
def add():
    db = get_db()
    dbase = todoDB(db)
    if request.method == 'POST':
        if len(request.form['todo']) > 4:
            res = dbase.addTodo(request.form['todo'], request.form['status'])
            if not res:
                flash('Ошибка добавления задачи', category = 'error')
            else:
                flash('Задача добавлена', category = 'succes')
        else:
            flash('Ошибка добавления задачи', category = 'error')
    return render_template('add.html')

@app.route('/edit/<id>', methods=['PATCH', 'GET'])
def edit(id):
    print('id ', id)
    db = get_db()
    dbase = todoDB(db)
    if request.method == 'PATCH':
        if len(request.form['todo']) > 4:
            res = dbase.updateTodo(request.form['todo'], request.form['status'], id)
            if not res:
                flash('Ошибка редактирования задачи', category = 'error')
            else:
                flash('Задача обновлена', category = 'succes')
                # index()
        else:
            flash('Ошибка добавления задачи', category = 'error')
    return render_template('edit.html', id = id, todo = dbase.getTodo(id))


if __name__ == "__main__":
    app.run()