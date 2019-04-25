from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.services.user_services import UserService
from app.services.template_service import TemplateService
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class PostForm(FlaskForm):
    name = StringField('Post name')
    body = TextAreaField('Post Body')
    submit = SubmitField('Submit Post')

class TemplateForm(FlaskForm):
    name = StringField('Template Name')
    css_file = FileField()
    submit = SubmitField('Submit Template')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    template = SelectField('Template', choices=[(template.name, template.name) for template in TemplateService().find_all_templates()])
    submit = SubmitField('Register')

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different username.')

    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different email address.')