from typing import Text
from flask_uploads import IMAGES
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField, SelectField,SubmitField
from wtforms.fields.simple import FileField
from wtforms.validators import Required,Email,EqualTo, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.widgets.core import FileInput




class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')



class BlogForm(FlaskForm):
    title = StringField('Title of your blog',validators=[Required()])
    blog = TextAreaField('Blog content',validators=[Required()])
    blog_category =SelectField("Blog category",choices=[('Lifestyle Blog','Lifestyle Blog'),('Business Blog','Business Blog'), ('Technology Blog','Technology Blog'), ('Fashion Blog','Fashion blog'),('Sports Blog','Sports Blog'), ('Other','Other')],validators=[Required()])    
    blog_image = FileField('Match your blog with an image')
    # submit = SubmitField('Post')

class CommentForm(FlaskForm):
    blog_comment = TextAreaField('Add a comment', validators=[Required()])
    submit = SubmitField('Post')

class SubscriberForm(FlaskForm):
    subscriber_email = StringField('Email Address',validators=[Required(),Email()])
    # submit = SubmitField('subscribe')
