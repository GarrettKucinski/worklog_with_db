import unittest
import worklog
import validation


class DBSetupTest(unittest.TestCase):
    def test_if_exists(self):
        assert worklog.Log.table_exists()


class CreationTest(unittest.TestCase):

    def test_bad_log_value(self):
        with self.assertRaises(ValueError):
            worklog.Log.create(task_name='This is a bad task',
                               first_name='Garrett',
                               last_name='Kucinski',
                               time_spent='forty',
                               notes='')


class SearchTest(unittest.TestCase):
    def setUp(self):
        self.search_query = 'Garrett'

    def test_date_validation(self):
        self.assertFalse(validation.validate_date_input(
            '02/20/1022'))
        self.assertTrue(validation.validate_date_input(
            '1022-01-30'))

    def test_time_spent_validation(self):
        self.assertFalse(validation.validate_time_spent('hello'))
        self.assertTrue(validation.validate_time_spent(40))


class MenuTest(unittest.TestCase):
    def setUp(self):
        self.menu = {'a': 'This is choice a', 'b': 'This is choice b'}

    def test_menu_choice(self):
        self.assertEqual(self.menu['a'], 'This is choice a')
        self.assertEqual(self.menu['b'], 'This is choice b')

    def test_get_user_choice(self):
        self.assertEqual('a', worklog.get_user_choice('a'))

    def test_validate_menu_choice(self):
        self.assertTrue(worklog.validate_menu_choice('a', self.menu))
        self.assertTrue(worklog.validate_menu_choice('b', self.menu))
        self.assertFalse(worklog.validate_menu_choice('c', self.menu))


if __name__ == "__main__":
    unittest.main()
