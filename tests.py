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
        self.assertFalse(validation.validate_valid_time_spent('hello'))
        self.assertTrue(validation.validate_time_spent(40))

    def test_search_input(self):
        self.assertFalse(worklog.search_by_date('hello'))
        self.assertTrue(worklog.search_by_date('1982-01-01'))

    def test_employee_search_input(self):
        self.assertFalse(worklog.search_by_employee(''))
        self.assertTrue(worklog.search_by_employee('Garrett'))

    def test_time_spent_search_input(self):
        self.assertFalse(worklog.search_by_time_spent('hello'))
        self.assertTrue(worklog.search_by_time_spent('40'))

    def test_term_search_input(self):
        self.assertFalse(worklog.search_by_term(''))
        self.assertTrue(worklog.search_by_term('this'))


class MenuTest(unittest.TestCase):

    def test_menu_choice(self):
        self.assertEqual(worklog.MAIN_MENU['a'], worklog.add_entry)
        self.assertEqual(worklog.MAIN_MENU['s'], worklog.search_entries)

    def test_search_function(self):
        self.assertEqual(worklog.search_entries(), menu_loop)

    def test_menu(self):
        self.assertTrue(menu_loop(menu=worklog.MAIN_MENU))

    def test_menu_loop_choice(self):
        worklog.menu_loop(menu=worklog.MAIN_MENU)
        self.assertTrue(choice='a')


if __name__ == "__main__":
    unittest.main()
