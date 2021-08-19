from . import main
from flask import render_template,request,redirect,url_for, abort
from flask_login import login_required, current_user 
from ..models import User, Blog, Comment
from .. import db,photos
from .forms import UpdateProfile, BlogForm, CommentForm



@main.route('/')
def index():
    '''
    Index page
    '''
    return render_template('index.html')

@main.route('/home', methods= ['POST', 'GET'])
@login_required
def home():
    '''
        home page view rendered after authentication process.
    '''
    blog_form = BlogForm()

    if blog_form.validate_on_submit():
        new_blog = Blog(blog_title = blog_form.title.data, blog_content = blog_form.blog.data, user=current_user)

        new_blog.save_blog()

        return redirect (url_for ("main.home"))
   
    blogs = Blog.query.all()    
    title = 'BlogPool Home'
    return render_template('home.html', title = title, blog_form = blog_form, blogs=blogs)


@main.route('/blog/blog-details/<int:id>',methods=['GET','POST'])
@login_required
def blog_details(id):
    single_blog=Blog.query.get(id)
    comments= Comment.query.filter_by(blog_id=id).all()
    commentForm=CommentForm()
    

    if commentForm.validate_on_submit():
        new_comment = Comment(blog_comment = commentForm.comment.data,blog_id=single_blog.blog_id, user=current_user)

        new_comment.save_comment()
    
        return redirect (url_for ("main.blog_details", id= single_blog.blog_id))


    
    return render_template('blog_details.html',comments=comments,single_blog=single_blog, commentForm=commentForm)

@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    blogs =Blog.query.filter_by(user=current_user)
    return render_template("profile/profile.html", blog = blogs,user=current_user)
