import unittest
from app.models import Pitch
from app import db
class PitchTest(unittest.TestCase):
    
    """
    Test class to test the behaviour of the Pitch
    """
    def setUp(self):
    
        """
        Set up method that will run before every Test
        """
        self.new_pitch = Pitch(0000, 'name','description')
        
    def test_instance(self):
        self.assertTrue(isinstance(self.new_pitch))
       
    def tearDown(self):
        Review.query.delete()
        User.query.delete() 