import unittest
from app.models import Quote
from app import db

class QuoteTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the Movie class
    '''

    def setUp(self):
        '''
        Set up method that will run before every Test
        '''
        self.new_quote = Quote(1,'Python is an OOP language','Mary John')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_quote,Quote))

    def test_to_check_instance_variables(self):
        self.assertEquals(self.new_quote.id,1)
        self.assertEquals(self.new_quote.quote,'Mary John')
        self.assertEquals(self.new_quote.author,'Python is an OOP language')
