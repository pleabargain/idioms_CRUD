import os
import random
from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

import json

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Idiom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phrase = db.Column(db.String(80), unique=True, nullable=False)
    context = db.Column(db.String(120), nullable=False)

# Rest of your code...


def create_database():
    if not os.path.exists('test.db'):
        with app.app_context():
            db.create_all()


current_idiom = None
previous_idiom = None

@app.route('/')
def home():
    global current_idiom
    idioms = Idiom.query.all()
    current_idiom = random.choice(idioms)
    return render_template('home.html', idiom=current_idiom)

@app.route('/next')
def next_idiom():
    global current_idiom, previous_idiom
    idioms = Idiom.query.all()
    previous_idiom = current_idiom
    current_idiom = random.choice(idioms)
    return render_template('home.html', idiom=current_idiom)

@app.route('/previous')
def previous_idiom():
    global previous_idiom
    return render_template('home.html', idiom=previous_idiom)


@app.route('/search', methods=['GET'])
def search_idiom():
    query = request.args.get('query')
    idioms = Idiom.query.filter(or_(Idiom.phrase.contains(query), Idiom.context.contains(query))).all()
    if not idioms:
        return render_template('not_found.html')
    return render_template('search_results.html', idioms=idioms)


@app.route('/add', methods=['POST'])
def add_idiom():
    data = request.form
    existing_idiom = Idiom.query.filter_by(phrase=data['phrase']).first()
    if existing_idiom is None:
        new_idiom = Idiom(phrase=data['phrase'], context=data['context'])
        db.session.add(new_idiom)
        db.session.commit()
        flash("The idiom was added to the database.")
        print(f"The idiom '{new_idiom.phrase}' was added to the database.")
    else:
        flash("An idiom with this phrase already exists.")
    return redirect(url_for('home'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_idiom(id):
    idiom = Idiom.query.get(id)
    if request.method == 'POST':
        data = request.form
        idiom.phrase = data['phrase']
        idiom.context = data['context']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit_idiom.html', idiom=idiom)



@app.route('/update/<int:id>', methods=['POST'])
def update_idiom(id):
    data = request.form
    idiom = Idiom.query.get(id)
    idiom.phrase = data['phrase']
    idiom.context = data['context']
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete/<int:id>')
def delete_idiom(id):
    idiom = Idiom.query.get(id)
    db.session.delete(idiom)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/import', methods=['POST'])
def import_json():
    file = request.files['file']
    data = json.load(file)
    for idiom in data['idioms']:
        phrase = idiom.get('phrase', '')  # Use an empty string if 'phrase' is not found
        context = idiom.get('context', '')  # Use an empty string if 'context' is not found
        new_idiom = Idiom(phrase=phrase, context=','.join(context) if isinstance(context, list) else context)
        db.session.add(new_idiom)
    db.session.commit()
    return redirect(url_for('home'))

@app.errorhandler(500)
def handle_500(error):
    return str(error), 500

def check_permissions():
    try:
        with open('tempfile', 'w') as f:
            pass
        os.remove('tempfile')
        return True
    except PermissionError:
        return False

def create_database():
    if check_permissions():
        if not os.path.exists('test.db'):
            with app.app_context():
                db.create_all()
            print("Database 'test.db' was successfully created in the current directory.")
    else:
        print("The application does not have permissions to create a database in this directory.")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, use_reloader=False)