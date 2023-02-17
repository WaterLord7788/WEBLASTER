from flask import Blueprint, request, flash, jsonify, flash, redirect, url_for
from flask import Flask, render_template, session
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
import json
import os
from .models import Note, Plant, Suggestion
from . import db

views = Blueprint('views', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/img/')
ADMIN = "kristian.paivinen@yahoo.com"


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note') #Gets the note from the HTML 
        if note:
            if len(note) < 1:
                flash('Note is too short!', category='error') 
            else:
                new_note = Note(data=note, user_id=current_user.id)  #Providing the schema for the note 
                db.session.add(new_note) #Adding the note to the database 
                db.session.commit()
                flash('Note added!', category='success')
        else:
            flash('No notes to add!', category='failure')

    return render_template("home.html", user=current_user, ADMIN=ADMIN)


@views.route('/plants', methods=['GET', 'POST'])
def plants():
    #print(Plant.query.all())
    if request.method == 'POST' and current_user.email == ADMIN:
        plant = request.form.get('plant') #Gets the plant from the HTML
        if plant:
            if len(plant) < 1:
                flash('Information regarding plant is too short!', category='error') 
            else:
                new_plant = Plant(data=plant)  #Providing the schema for the plant 
                db.session.add(new_plant) #Adding the plant to the database 
                db.session.commit()
                flash('Plant added!', category='success')
        else:
            flash('No plants to add!', category='failure')
    elif request.method == 'POST' and current_user.email != ADMIN and current_user.email != None:
        plant = request.form.get('plant') #Gets the plant from the HTML
        if plant:
            if len(plant) < 1:
                flash('Information regarding plant is too short!', category='error') 
            else:
                new_suggestion = Suggestion(data=plant)  #Providing the schema for the plant 
                db.session.add(new_suggestion) #Adding the plant to the database 
                db.session.commit()
                flash('Suggestion added!', category='success')
        else:
            flash('No suggestions to add!', category='failure')
    plants = Plant.query.all()
    return render_template("plants.html", user=current_user, plants=plants)


### EXPIREMENTAL ###
@views.route('/suggestions', methods=['GET', 'POST'])
def suggestions():
    #print(Suggestion.query.all())
    if request.method == 'POST' and current_user.email != ADMIN and current_user.email != None:
        suggestion = request.form.get('suggestion')
        if suggestion:
            if len(suggestion) < 1:
                flash('Information regarding new suggestion is too short!', category='error') 
            else:
                new_suggestion = Suggestion(data=suggestion)
                db.session.add(new_suggestion)
                db.session.commit()
                flash('Suggestion added!', category='success')
        else:
            flash('No suggestions to add!', category='failure')
    suggestions = Suggestion.query.all()
    return render_template("suggestions.html", user=current_user, suggestions=suggestions)
### EXPIREMENTAL ###


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@views.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return '''
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
            integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous"/>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"
            crossorigin="anonymous"/>
            <upload-image>
                <div align="center" class="alert alert-danger" role="alert">
                    <b>No file part</b>
                    <form id="imageform" method="POST" enctype="multipart/form-data" action="http://127.0.0.1:5000/upload">
                    <div>
                        <input id="file" type="file" name="file" />
                        <button id="upload-button" class="btn btn-primary">Upload image</button>
                    </div>
                    </form>
                    <br>
                </div>
            </upload-image>
            '''
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            response = '''
                    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
                    integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous"/>
                    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"
                    crossorigin="anonymous"/>
                    <upload-image>
                        <div align="center" class="alert alert-success" role="alert">
                            <b>Successful upload!</b>
                            <a href="http://127.0.0.1:5000/static/img/'''+file.filename+'''" target="_blank">Check it out.</a>
                            <form id="imageform" method="POST" enctype="multipart/form-data" action="http://127.0.0.1:5000/upload">
                            <div>
                                <input id="file" type="file" name="file" />
                                <button id="upload-button" class="btn btn-primary">Upload image</button>
                            </div>
                            <p>
                                <b>HTML code:</b> 
                                &lt;img src="http://127.0.0.1:5000/static/img/'''+file.filename+'''" 
                                                    align="center"&gt;
                            </p>
                            </form>
                        </div>
                    </upload-image>
                   '''
            return response
        else:
            return '''
                    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
                    integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous"/>
                    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"
                    crossorigin="anonymous"/>
                    <upload-image>
                        <div align="center" class="alert alert-warning" role="alert">
                            <b>Forbidden extension</b>
                            <form id="imageform" method="POST" enctype="multipart/form-data" action="http://127.0.0.1:5000/upload">
                            <div>
                                <input id="file" type="file" name="file" />
                                <button id="upload-button" class="btn btn-primary">Upload image</button>
                            </div>
                            </form>
                        </div>
                    </upload-image>
                   '''
    return '''
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
            integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous"/>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"
            crossorigin="anonymous"/>
            <upload-image>
                <div align="center" class="alert alert-primary" role="alert">
                    <b>Upload an image!</b><br>
                    <i>You will get a link and a piece of HTML to copy-paste into your note</i>
                    <form id="imageform" method="POST" enctype="multipart/form-data" action="http://127.0.0.1:5000/upload">
                    <div>
                        <input id="file" type="file" name="file" />
                        <button id="upload-button" class="btn btn-primary">Upload image</button>
                    </div>
                    </form>
                    <br>
                </div>
            </upload-image>
            '''


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


@views.route('/delete-plant', methods=['POST'])
def delete_plant():  
    plant = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    plantId = plant['plantId']
    plant = Plant.query.get(plantId)
    if plant:
        if current_user.email == ADMIN:
            db.session.delete(plant)
            db.session.commit()
            flash('Plant deleted!', category='success')
    return jsonify({})


@views.route('/accept-suggestion', methods=['POST'])
def accept_suggestion():
    suggestion = json.loads(request.data) # The ID of the suggestion
    suggestionId = suggestion['suggestionId']
    suggestionData = Suggestion.query.get(suggestionId).data
    suggestionDate = Suggestion.query.get(suggestionId).date
    suggestionUserID = Suggestion.query.get(suggestionId).user_id
    suggestion = Suggestion.query.get(suggestionId) # Rewriting it to be a new value
    #print(suggestionId)
    #print(Suggestion.query.get(suggestionId).id)
    #plant = Suggestion.query.get(suggestionId)
    new_plant = Plant(id=suggestionId, data=suggestionData, date=suggestionDate, user_id=suggestionUserID)

    if new_plant:
        if current_user.email == ADMIN:
            #new_plant = Plant(data=plant)  #Providing the schema for the plant
            db.session.add(new_plant) #Adding the plant to the database
            db.session.delete(suggestion)
            db.session.commit()
            flash('Suggestion accepted and a new plant created!', category='success')


    return jsonify({})


@views.route('/delete-suggestion', methods=['POST'])
def delete_suggestion():
    suggestion = json.loads(request.data) # this function expects a JSON from the INDEX.js file
    suggestionId = suggestion['suggestionId']
    suggestion = Suggestion.query.get(suggestionId)
    if suggestion:
        if current_user.email == ADMIN:
            db.session.delete(suggestion)
            db.session.commit()
            flash('Suggestion deleted!', category='success')
    return jsonify({})