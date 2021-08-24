from app.requests import get_quote
from . import main
from flask import render_template,request,redirect,url_for, abort, flash
from flask_login import login_required, current_user 
from ..models import Quote, Subscriber, User, Blog, Comment
from .. import db,photos
from .forms import SubscriberForm, UpdateProfile, BlogForm, CommentForm
import markdown2 
from ..email import mail_message
from sqlalchemy import desc
from werkzeug import secure_filename



@main.route('/')
def index():
    '''
    Index page
    '''
    blog_one = Blog.query.filter_by(blog_id=1).first()
    blog_two = Blog.query.filter_by(blog_id=2).first()
    blog_three = Blog.query.filter_by(blog_id=3).first()
    quote = get_quote()
    
    title = 'BlogPool'
    return render_template('index.html', quote=quote, blog_one =blog_one, blog_two = blog_two, blog_three =blog_three, title=title)

@main.route('/home', methods= ['POST', 'GET'])
@login_required
def home():
    '''
        home page view rendered after authentication process.
    '''   
    # blogs = Blog.query.all()
    blogs = Blog.query.order_by(Blog.datetime_posted.desc()).all()
    # if blogs is None:
    #     abort(404)
    #format_blog = markdown2.markdown(blogs.blog_content,extras=["code-friendly", "fenced-code-blocks"])
   
    title = 'BlogPool Home'
    return render_template('home.html', title = title, blogs=blogs)


@main.route('/blog/blog-details/<int:id>',methods=['GET','POST'])
@login_required
def blog_details(id):
    single_blog=Blog.query.get(id)
    comments= Comment.query.filter_by(blog_id=id).all()
    # comments = Comment.query.order_by(Comment.datetime_posted.desc()).all

    commentForm=CommentForm()
    

    if commentForm.validate_on_submit():
        new_comment = Comment(blog_comment = commentForm.blog_comment.data,blog_id=single_blog.blog_id, user=current_user)

        new_comment.save_comment()
    
        return redirect (url_for ("main.blog_details", id= single_blog.blog_id))


    title = 'Blog Details'

    return render_template('blog_details.html',comments=comments,single_blog=single_blog, commentForm=commentForm, title=title)

@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    blogs =Blog.query.filter_by(user=current_user)
    return render_template("profile/profile.html", blogs = blogs,user=current_user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic = path
        db.session.commit()
        return redirect(url_for('main.profile',uname=uname))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods=['GET','POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic = path
        db.session.commit()
        return redirect(url_for('main.profile',uname=uname))

@main.route('/blog-submission',methods=['GET','POST'])
@login_required
def blog_submission():
    blog_form = BlogForm()
    sub_form = SubscriberForm()
    if blog_form.validate_on_submit():
        new_blog = Blog(
            blog_title = blog_form.title.data, 
            blog_content = blog_form.blog.data, 
            blog_category = blog_form.blog_category.data, 
            blog_image = blog_form.blog.data,
            user=current_user)
    
        new_blog.save_blog()

        subscribers=Subscriber.query.all()

        for subscriber in subscribers:
            mail_message("New Blog Post","email/newPost/newPostAlert", subscriber.subscriber_email,blog=new_blog)

        return redirect (url_for ("main.home"))

    if sub_form.validate_on_submit():
        new_subscriber = Subscriber(
            subscriber_email = sub_form.subscriber_email.data
        )

        new_subscriber.save_subscriber()
        flash('You have been successfully subscribed')
        mail_message("Subscription alert","email/welcomeSubscriber/welcome_subscriber",new_subscriber.subscriber_email,subscriber=new_subscriber)

        return redirect (url_for ("main.blog_submission"))
    
    title = 'Blog Submission'
    return render_template('blog_submission.html', title = title, blog_form=blog_form, sub_form = sub_form)


@main.route('/blog/editblog/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_blog(id):
    """
    Edit a blogpost
    """
    blogs = Blog.query.filter_by(blog_id = id).first()
    if request.method == 'post':
        blog_title = request.form['blog_title']
        blog_category = request.form['blog_category']
        blog_content = request.form['blog_content'] 

        db.session.commit()
        return redirect(url_for('main.home'))
        
    title = "Update Post"
    return render_template('blog_update.html', title = title, blogs=blogs)




@main.route('/blog/delete/<int:id>')
@login_required
def delete_blog(id):
    blog = Blog.query.filter_by(blog_id =id).first()
    if current_user.id == blog.user.id:
        db.session.delete(blog)
        db.session.commit()

    return redirect(url_for('main.home'))


@main.route('/blog/comment/delete/<int:id>')
@login_required
def delete_comment(id):

    comment = Comment.query.filter_by(id =id).first()
    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for('main.blog_details', id = comment.blog_id))



@main.route('/Business')
@login_required
def business():

    title = 'Business Blogs'
    h4 = 'Business Blogs'
    random = "Business Blog"
    blogs = Blog.query.filter_by(blog_category =random).all()

    return render_template('blog_categories.html', title = title, blogs=blogs, h4 =h4)

@main.route('/lifestyle')
@login_required
def lifestyle():

    title = 'Lifestyle Blogs'
    h4 = 'Lifestyle Blogs'
    random = "Lifestyle Blog"
    blogs = Blog.query.filter_by(blog_category =random).all()
    return render_template('blog_categories.html', title = title, blogs=blogs, h4 =h4)


@main.route('/technology')
@login_required
def technology():

    title = 'Technology-Blogs'
    h4 = 'Technology Blogs'
    random = "Technology Blog"
    blogs = Blog.query.filter_by(blog_category =random).all()
    return render_template('blog_categories.html', title = title, blogs=blogs, h4 =h4)
    
@main.route('/fashion')
@login_required
def fashion():

    title = 'Fashion-Blogs'
    h4 = 'Fashion Blogs'
    random = "Fashion Blog"
    blogs = Blog.query.filter_by(blog_category =random).all()
    return render_template('blog_categories.html', title = title, blogs=blogs, h4 =h4)

@main.route('/entertainment')
@login_required
def entertainment():
    
    title = 'Entertainment Blogs'
    h4 = 'Entertainment Blogs'
    random = "Entertainment Blog"
    blogs = Blog.query.filter_by(blog_category =random).all()
    return render_template('blog_categories.html', title = title, blogs=blogs, h4 =h4)


@main.route('/sports')
@login_required
def sports():

    title = 'Sports-Blogs'
    h4 = 'Sports Blogs'
    random = "Sports Blog"
    blogs = Blog.query.filter_by(blog_category =random).all()
    return render_template('blog_categories.html', title = title, blogs=blogs, h4 =h4)

@main.route('/Others')
@login_required
def other():

    title = 'Other Blogs'
    h4 = 'Other Blogs'
    random = "Other Blog"
    blogs = Blog.query.filter_by(blog_category =random).all()
    return render_template('blog_categories.html', title = title, blogs=blogs, h4 =h4)

    


