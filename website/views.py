from flask import Blueprint, render_template, request, flash, jsonify, url_for, redirect
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


# views.py

# ... Other imports ...

# views.py

# ... Other imports ...

@views.route('/edit-note/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get(note_id)

    if note is None:
        flash('Note not found', category='error')
        return redirect(url_for('views.home'))

    # Check if the current user is the owner of the note
    if note.user_id != current_user.id:
        flash('Permission denied', category='error')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        new_content = request.form.get('new_content')
        print(f"New content received: {new_content}")  # Add this line for debugging

        if new_content is not None:  # Check if new_content is not None
            note.data = new_content
            db.session.commit()
            flash('Note updated successfully', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('Note content cannot be empty', category='error')

    return render_template("edit_note.html", user=current_user, note=note)
