import unittest
from app.models import Post,User
from app import db


class PostTest(unittest.TestCase):

    def setUp(self):
        self.user_user_Test = User(username = 'Test',password = 'bread', email = 'test@gmail.com')
        self.new_post= Post(id=12,title='Title',author_id =13)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_post,Post))


    def test_to_check_instance_variables(self):
        self.assertEquals(self.new_post.id,12)
        self.assertEquals(self.new_post.title,'Title')
        self.assertEquals(self.new_post.author_id,13)
        