from flask import Flask, render_template
from flask_bootstrap import Bootstrap
app = Flask(__name__)

bootstrap = Bootstrap(app)


@app.route('/')
def index():
    test_list = {'name': 'dog','fname': 'cat', 'last': 'fish'}
    return render_template('index.html', test_list=test_list)

