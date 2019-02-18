import unittest
from app.models import Comment,User,Post
from app import db

class CommentModelTest(unittest.TestCase):
    def setUp(self):
        self.user_Test = User(username = 'Test',password = 'bread', email = 'test@gmail.com')
        self.post_New = Post(title = 'New',body = 'blog', id = '1')
        self.new_comment = Comment(body = 'cool stuff',author='Mary John')

    def tearDown(self):
        Comment.query.delete()
        Post.query.delete()
        User.query.delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment,Comment))

    def test_to_check_instance_variables(self):
      
        self.assertEquals(self.new_comment.body,'cool stuff')
        self.assertEquals(self.new_comment.author,'Mary John')
        
