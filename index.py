from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import my_functions

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my little secret'

bootstrap = Bootstrap(app)

class NameForm(FlaskForm):
    name = StringField('Type artist name', validators=[DataRequired()])
    submit = SubmitField('Insert new artist data to DB')

class DbForm(FlaskForm):
    limit = StringField('Type number of rows', validators=[DataRequired()])
    submit = SubmitField('Get data from DB')

band = 'beatles'

@app.route('/', methods=['GET', 'POST'])
def index():
    
    
    #artist_id = my_functions.get_artist_id(band)
    songs = my_functions.get_from_table()
      

 #Put new data to database   
    name = None
    nameform = NameForm()
    if nameform.validate_on_submit():
        name = nameform.name.data
        nameform.name.data = ''
        band = name
        
        my_functions.drop_table()
        my_functions.create_table()
        artist_id = my_functions.get_artist_id(band)
        songs = my_functions.get_artist_songs(artist_id, limit=500)
        my_functions.fill_table(songs)
        songs = my_functions.get_from_table()

 # Get data from database   
    limit1 = None
    dbform = DbForm()
    if dbform.validate_on_submit():
        limit1 = dbform.limit.data
        dbform.limit.data = ''
        limit = limit1
        songs = my_functions.get_from_table(limit=limit)
        

    
    return render_template('index.html', songs=songs, band=band, nameform=nameform, dbform=dbform)

