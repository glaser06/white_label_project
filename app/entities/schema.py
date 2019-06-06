
from marshmallow import Schema, fields, post_load
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, object):
    def __init__(self, username, email, template_id='', id='', password_hash=''):
        self.username = username
        self.email = email
        self.id = id
        self.password_hash = password_hash
        self.template_id = template_id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "User " + self.username


class UserSchema(Schema):
    id = fields.Str()
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password_hash = fields.Str()
    template_id = fields.Str()

    @post_load
    def make_user(self, data):
        return User(**data)


class Post(object):
    def __init__(self, name, body, user_id='', id=''):
        self.id = id
        self.name = name
        self.body = body
        self.user_id = user_id


class PostSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    body = fields.Str()
    user_id = fields.Str()
    @post_load
    def make_post(self, data):
        return Post(**data)


class Template(object):
    def __init__(self, name, main_css_url='', logo_img_url='', id=''):
        self.id = id
        self.name = name
        self.main_css_url = main_css_url
        self.logo_img_url = logo_img_url


class TemplateSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    main_css_url = fields.Str()
    logo_img_url = fields.Str()
    @post_load
    def make_template(self, data):
        return Template(**data)
