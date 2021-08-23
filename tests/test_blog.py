import unittest
from app.models import Blog, Comment, User
from flask_login import current_user
from app import db

class TestBlog(unittest.TestCase):

    def setUp(self):
        self.user_frank = User(id= 3,first_name= 'Franklin',last_name ='Mutua', username = "Frankfreek", email ="franklinngumbi@gmail.com", bio = "Just stay there", profile_pic = "image_url", password = '12345')
        self.new_blog = Blog(blog_id=5, blog_title='The rise and downfall of Sonko', blog_category='Entertainment blog', blog_content ='This is how it goes', datetime_posted = '15/6/2021', blog_image ='blog_image_url', user_id = 3)



    def tearDown(self):
        Blog.query.delete()
        User.query.delete()


    def test_instance(self):
        self.assertTrue(isinstance(self.new_blog,Blog))


    def test_check_instance_variables(self):
        self.assertEquals(self.new_blog.blog_id,2)
        self.assertEquals(self.new_blog.blog_title,'The rise and downfall of Sonko')
        self.assertEquals(self.new_blog.blog_category,'Entertainment blog')
        self.assertEquals(self.new_blog.blog_content,'This is how it goes')
        self.assertEquals(self.new_blog.datetime_posted,'15/6/2021')
        self.assertEquals(self.new_blog.blog_image,'blog_image_url')
        self.assertEquals(self.new_blog.user_id, 3)
     

  
    def test_save_blog(self):
        db.session.add(self.user_frank)
        db.session.commit()
        self.new_blog.save_blog()
        self.assertTrue(len(Blog.query.all())==1)
