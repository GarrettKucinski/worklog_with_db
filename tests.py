import unittest
import worklog


class DBSetupTest(unittest.TestCase):
    def test_if_exists(self):
        assert worklog.Log.table_exists()


class SearchTest(unittest.TestCase):
    def setUp(self):
        self.search_query = 'Garrett'

    def test_bad_log_value(self):
        name = 'This is a bad task'
        user_fname = 'Garrett'
        user_lname = 'Kucinski'
        task_time = 'forty'
        task_notes = ''

        with self.assertRaises(ValueError):
            worklog.Log.create(task_name=name,
                               first_name=user_fname,
                               last_name=user_lname,
                               time_spent=task_time,
                               notes=task_notes)

    def test_bad_search_date(self):
        self.assertFalse(worklog.search_by_date(search_query='02/20/1022'))

    def test_bad_search_time_spent(self):
        self.assertFalse(worklog.search_by_time_spent(
            search_query='02/20/1022'))

    def test_bad_search_employee(self):
        self.assertFalse(worklog.search_by_employee(search_query=''))

    def test_bad_search_term(self):
        self.assertFalse(worklog.search_by_date(search_query=''))


class MenuTest(unittest.TestCase):
    def setUp(self):
        self.main_menu_choice_a = worklog.add_entry
        self.main_menu_choice_s = worklog.search_entries

    def test_main_menu_choice(self):
        self.assertEqual(self.main_menu_choice_a, worklog.MAIN_MENU['a'])
        self.assertEqual(self.main_menu_choice_s, worklog.MAIN_MENU['s'])


if __name__ == "__main__":
    unittest.main()
