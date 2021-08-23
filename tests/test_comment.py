import unittest
from app.models import Blog, Comment
from flask_login import current_user
from app import db

class TestComment(unittest.TestCase):

    def setUp(self):
        self.new_blog = Blog(blog_id=5, blog_title='The rise and downfall of Sonko', blog_category='Entertainment blog', blog_content ='This is how it goes', datetime_posted = '15/6/2021', blog_image ='blog_image_url', user_id = 3)
        self.new_comment = Comment(id =3, blog_id=5, blog_comment ='Great stuff', datetime_posted ='17/6/2021', user_id=3)


    def tearDown(self):
        Comment.query.delete()
        Blog.query.delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment,Comment))


    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.id,3)
        self.assertEquals(self.new_comment.blog_id,5)
        self.assertEquals(self.new_comment.blog_comment, 'Great stuff')
        self.assertEquals(self.new_comment.datetime_posted,'17/6/2021')
        self.assertEquals(self.new_comment.user_id,3)


  
    def test_save_comment(self):
        db.session.add(self.new_blog)
        db.session.commit()
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)
