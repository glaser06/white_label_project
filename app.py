import os
from flask import Flask, url_for
from flask import render_template
app = Flask(__name__)
app.config['SERVER_NAME'] = 'example.com:5000'

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.route('/')
def hello_world(): 
    return "Hello world!!"
@app.route('/', subdomain="<name>")
def hello_blog(name): 
    if name in ["white", "green"] : 

        return render_template('hello.html', name=name, static_url=url_for('static', filename=name+'/css/main.css'))
    return render_template('hello.html', name=name, static_url=url_for('static', filename='default/css/main.css'))
    return "Hello" + name + "!!"
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    if name in ["white", "green"] : 

        return render_template('hello.html', name=name, static_url=url_for('static', filename=name+'/css/main.css'))
    return render_template('hello.html', name=name, static_url=url_for('static', filename='default/css/main.css'))





