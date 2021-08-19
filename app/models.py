from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    username = db.Column(db.String(255),index = True,nullable=False)
    email = db.Column(db.String(255),unique = True,index = True,nullable=False)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255),nullable=False)
    profile_pic = db.Column(db.String(),nullable=False)
    password_secure = db.Column(db.String(255),nullable=False)
    blogs = db.relationship('Blog',backref = 'user',lazy = "dynamic")
    comments = db.relationship('Comment',backref = 'user',lazy = "dynamic")

   
    
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_secure = generate_password_hash(password)


    def verify_password(self,password):
        print(self.password_secure)
        return check_password_hash(self.password_secure,password)

        
    def __repr__(self):
        return f'User {self.username}'


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")


    def __repr__(self):
        return f'User {self.name}'

class Blog(db.Model):
    __tablename__ = 'blogs'
    blog_id = db.Column(db.Integer,primary_key = True, autoincrement=True)
    blog_title = db.Column(db.String, nullable=False)
    blog_content = db.Column(db.String, nullable=False)
    datetime_posted = db.Column(db.DateTime,default=datetime.now())
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    blog_comments = db.relationship('Comment',backref = 'comment',lazy="dynamic")




    def save_blog(self):
        """
        method saves new blog objects into the blog db table
        """
        db.session.add(self)
        db.session.commit()

    def delete_blog(self):
        """
        method deletes blog from the blog db table 
        """
        single_blog = Blog.query.filter_by(id = 1).first()
        db.session.delete(single_blog)
        db.session.commit()



    @classmethod
    def display_blogs(cls,blog_id):
        blogs = Blog.query.filter_by(blog_id=blog_id).all()
        return blogs

class Comment(db.Model):
    
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key = True, autoincrement= True)
    blog_id = db.Column(db.Integer, db.ForeignKey("blogs.blog_id"))
    blog_comment = db.Column(db.String, nullable=False)
    datetime_posted = db.Column(db.DateTime,default=datetime.now())
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))



    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    def delete_comment(self):
        single_comment = Comment.query.filter_by(id = 1).first()
        db.session.delete(single_comment)
        db.session.commit()



    @classmethod
    def display_comments(cls, id):

        comments = Comment.query.filter_by(blog_id= id).all()
        return comments




