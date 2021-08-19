from typing import Text
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField, SelectField,SubmitField
from wtforms.validators import Required
from wtforms.ext.sqlalchemy.fields import QuerySelectField




class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')



class BlogForm(FlaskForm):
    title = StringField('Enter the title of your blog',validators=[Required()])
    blog = TextAreaField('Enter your blog content',validators=[Required()])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    comment = TextAreaField('Add a comment', validators=[Required()])
    submit = SubmitField('Post')
