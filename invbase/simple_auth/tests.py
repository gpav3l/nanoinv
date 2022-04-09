from django.test import TestCase
from .service import *

persons_dict = [
    {'fio':"Иванов Иван", 'login':"admin", 'pass':"admin", 'config':{}},
    {'fio': "Сидоров Сидр", 'login': "user", 'pass': "user", 'config': {}},
]

class AuthorithationTestCase(TestCase):
    def setUp(self):
        for p in persons_dict:
            Personal.objects.create(fio=p['fio'], login=p['login'], pass_hash=hashlib.md5(p['pass'].encode()).hexdigest(), config=p['config'])

    '''
    def test_empty_login_and_password(self):
        self.assertEqual(check_input("", ""), False)
        self.assertEqual(check_input("admin", ""), False)
        self.assertEqual(check_input("", "admin"), False)
        self.assertEqual(check_input("   ", "admin"), False)
        self.assertEqual(check_input(" ", "  "), False)

    def test_nonempty_login_and_password(self):
        self.assertEqual(check_input("admin", "admin"), True)
        self.assertEqual(check_input("' or 1=1 --", ";*ererewr"), False)
    '''

    def test_get_person(self):
        # Check to item from base
        for p in persons_dict:
            self.assertEqual(get_person(p['login'], p['pass']), p['fio'])

        # Check item not from base
        self.assertEqual(get_person("admin", ""), "")
        self.assertEqual(get_person("' or 1=1 --", "123"), "")
        self.assertEqual(get_person("user", "-----"), "")
        self.assertEqual(get_person("  ", "123"), "")
        self.assertEqual(get_person(" ", " "), "")