import sys
sys.path.append('../')
# import os.path
# import sys
# import time

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
# from flask import Flask, json, g, request

# from app.entities.schema import PostSchema


import os
from flask import Flask, url_for, Blueprint
from flask import render_template, flash, redirect
from .forms import LoginForm, RegistrationForm, PostForm, TemplateForm
from flask_login import LoginManager
from flask_login import current_user, login_user, logout_user, login_required
from app.services.user_services import UserService
from app.services.post_service import PostService
from app.services.template_service import TemplateService
from app.entities.schema import UserSchema, PostSchema
from flask import request
from werkzeug.urls import url_parse

app = Flask(__name__)
app.config['SECRET_KEY'] = 'big_secret'
# app.config['SERVER_NAME'] = 'random-python.appspot.com'
app.config['SERVER_NAME'] = 'example.com:5000'
login = LoginManager(app)
login.login_view = 'login'

user_service = UserService()
post_service = PostService()
template_service = TemplateService()

# app = Blueprint('web_server', __name__, template_folder='templates')



@login.user_loader
def load_user(id):

    return user_service.find_user(id)

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
def index():
    if current_user.is_authenticated:
        return render_template('index.html', users=[current_user.username])    
    users = user_service.find_all_users()
    return render_template('index.html', users=[user.username for user in users], static_url=url_for('static', filename='default/css/main.css'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: 
        return redirect(url_for('index')) 
    form = LoginForm()

    if form.validate_on_submit():

        user = user_service.find_user_by_name(form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = "http://"+current_user.username+'.'+app.config['SERVER_NAME']
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user_data = {
            'username': form.username.data, 
            'email': form.email.data,
        }
        
        user_service.create_user_for(user_data, form.password.data, form.template.data)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/', subdomain="<name>")
@login_required
def profile(name): 
    template = template_service.find_templates_for_user(current_user)
    raw_posts = post_service.find_posts_by_user(current_user)
    posts = [PostSchema(exclude=['id','user_id']).dump(post).data for post in raw_posts]

    print(raw_posts)
    if template.main_css_url == 'local':
        return render_template('profile.html', static_url=url_for('static', filename=template.name+'/css/main.css'), posts=posts)
    elif template.main_css_url != "":
        return render_template('profile.html', static_url=template.main_css_url, posts=posts)
    else:
        return render_template('profile.html', static_url=url_for('static', filename='default/css/main.css'))


@app.route('/post/create', methods=['GET','POST'])
@login_required
def create_post(): 
    form = PostForm()
    if form.validate_on_submit():
        post_data = {
            'name': form.name.data,
            'body': form.body.data,
        }
        post_service.create_post_for(current_user, post_data)
        return redirect("http://"+current_user.username+'.'+app.config['SERVER_NAME'])
    return render_template('create_post.html', title='Create Post', form=form)
    
@app.route('/template/create', methods=['GET','POST'])
@login_required
def create_template(): 
    form = TemplateForm()
    if form.validate_on_submit():
        template_data = {
            'name': form.name.data,
        }
        uploaded_file = form.css_file.data
        template_service.create_template(template_data, uploaded_file)
        return redirect("http://"+current_user.username+'.'+app.config['SERVER_NAME'])
    return render_template('create_template.html', title='Create Template', form=form)
           
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    if name in ["white", "green"] : 

        return render_template('hello.html', name=name, static_url=url_for('static', filename=name+'/css/main.css'))
    return render_template('hello.html', name=name, static_url=url_for('static', filename='default/css/main.css'))
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')




