import sqlite3
import os
import random

from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row

    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()

    conn.close()

    if post is None:
        abort(404)
    return post


app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()

    return render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)

    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        titulo = request.form['title']
        conteudo = request.form['content']

        if not titulo:
            flash('O título é obrigadótio. Por favor, informe!')

        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (titulo, conteudo))

            conn.commit()
            conn.close()

            return redirect(url_for('index'))

    return render_template('create.html')


if __name__ == "__main__":
    app.run(debug=True)
