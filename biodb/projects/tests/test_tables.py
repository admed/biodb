from django.test import TestCase
from projects.tables import CustomCheckBoxColumn
from bs4 import BeautifulSoup

class CustomCheckBoxColumnTests(TestCase):
    @classmethod
    def setUpClass(cls):
        ''' Create imitation of record instance required by modify_input_name method '''
        super(CustomCheckBoxColumnTests, cls).setUpClass()

        class Record:
            id = 1234

        cls.record = Record() 

    def test_modify_input_name_method(self):
        ''' Test the way method create input name and the name it set '''

        old_input = '<input type="checkbox" name="random" value="m3">'
        new_input = CustomCheckBoxColumn.modify_input_name(old_input, self.record)

        soup = BeautifulSoup(new_input, 'html.parser')
        tag = soup.input
        self.assertEqual(tag["name"], "robject_1234") 


