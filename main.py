import os
import random
from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError



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
    # Pass the query to the template
    return render_template('search_results.html', idioms=idioms, query=query)


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
        # Redirect to the show_idiom route with the id of the new idiom
        return redirect(url_for('show_idiom', id=new_idiom.id))
    else:
        flash("An idiom with this phrase already exists.")
    return redirect(url_for('home'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_idiom(id):
    idiom = Idiom.query.get_or_404(id)
    if request.method == 'POST':
        idiom.phrase = request.form['phrase']
        idiom.context = request.form['context']
        db.session.commit()
        return redirect(url_for('next_idiom'))
    return render_template('edit.html', idiom=idiom)



from flask import request, redirect, url_for

from flask import flash

@app.route('/update_idiom/<int:id>', methods=['POST'])
def update_idiom(id):
    # Get the idiom from the database
    idiom = Idiom.query.get(id)

    if idiom:
        try:
            # Update the idiom's fields with the form data
            idiom.phrase = request.form['phrase']
            idiom.context = request.form['context']

            # Save the changes to the database
            db.session.commit()

            print('Idiom updated')  # This will print to the server's console

            # Notify the user that the update was successful
            flash('Idiom updated successfully!')

        except Exception as e:
            # If an error occurred, roll back the transaction
            db.session.rollback()

            print('Error updating idiom: ', e)  # This will print to the server's console

            # Notify the user that the update failed
            flash('An error occurred while updating the idiom. Please try again.')

        # Redirect the user to the idiom page
        return redirect(url_for('show_idiom', id=id))

    else:
        # Handle the case where the idiom doesn't exist
        flash('Idiom not found.')
        return redirect(url_for('home'))

@app.route('/show/<int:id>')
def show_idiom(id):
    idiom = Idiom.query.get_or_404(id)
    return render_template('show_idiom.html', idiom=idiom)

@app.route('/delete/<int:id>')
def delete_idiom(id):
    idiom = Idiom.query.get(id)
    db.session.delete(idiom)
    db.session.commit()
    return redirect(url_for('home'))


# from sqlalchemy.exc import IntegrityError

@app.route('/import', methods=['POST'])
def import_json():
    file = request.files['file']
    new_entries = 0  # Counter for new entries
    if file and file.read(1):
        file.seek(0)  # Reset file pointer to beginning
        data = json.load(file)
        for idiom in data['idioms']:
            phrase = idiom.get('phrase', '')  # Use an empty string if 'phrase' is not found
            context = idiom.get('context', '')  # Use an empty string if 'context' is not found
            new_idiom = Idiom(phrase=phrase, context=','.join(context) if isinstance(context, list) else context)
            db.session.add(new_idiom)
            try:
                db.session.commit()
                new_entries += 1  # Increment the counter
            except IntegrityError:
                db.session.rollback()  # Rollback the session if a duplicate is found
    else:
        flash("The file is empty.")
    return render_template('import_report.html', new_entries=new_entries)

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