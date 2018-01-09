import unittest
import worklog


class DBSetupTest(unittest.TestCase):
    def test_if_exists(self):
        assert worklog.Log.table_exists()


class SearchTest(unittest.TestCase):
    def setUp(self):
        self.search_query = 'Garrett'

    def test_bad_log_value(self):
        with self.assertRaises(ValueError):
            worklog.Log.create(task_name='This is a bad task',
                               first_name="Garrett",
                               last_name="Kucinski",
                               time_spent='forty',
                               notes="")
