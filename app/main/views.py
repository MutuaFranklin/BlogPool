from . import main
from flask import render_template,request,redirect,url_for, abort, flash
from flask_login import login_required, current_user 
from ..models import Subscriber, User, Blog, Comment
from .. import db,photos
from .forms import SubscriberForm, UpdateProfile, BlogForm, CommentForm
import markdown2 




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
    blogs = Blog.query.all() 
    # if blogs is None:
    #     abort(404)
    # format_blog = markdown2.markdown(blogs.blog_content,extras=["code-friendly", "fenced-code-blocks"])
   
    title = 'BlogPool Home'
    return render_template('home.html', title = title, blogs=blogs)


@main.route('/blog/blog-details/<int:id>',methods=['GET','POST'])
@login_required
def blog_details(id):
    single_blog=Blog.query.get(id)
    comments= Comment.query.filter_by(blog_id=id).all()
    commentForm=CommentForm()
    

    if commentForm.validate_on_submit():
        new_comment = Comment(blog_comment = commentForm.blog_comment.data,blog_id=single_blog.blog_id, user=current_user)

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

@main.route('/blog-submission',methods=['GET','POST'])
@login_required
def blog_submission():
    blog_form = BlogForm()
    sub_form = SubscriberForm()

    if blog_form.validate_on_submit():
        new_blog = Blog(
            blog_title = blog_form.title.data, 
            blog_content = blog_form.blog.data, 
            user=current_user)

        new_blog.save_blog()

        return redirect (url_for ("main.home"))

    if sub_form.validate_on_submit():
        new_subscriber = Subscriber(
            subscriber_email = sub_form.subscriber_email.data, 
        )

        new_subscriber.save_subscriber()
        flash('You have been successfully subscribed')


        return redirect (url_for ("main.blog_submission"))
    
    title = 'Blog Submission'
    return render_template('blog_submission.html', title = title, blog_form=blog_form, sub_form = sub_form)
