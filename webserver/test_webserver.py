import unittest
from webserver.models import db


class LojnoteWebserverTestCases(unittest.TestCase):

    def test_db(self):
        conn, meta = db.connect('masato', '', 'masato', host='localhost', port=5432)
        self.assertIsNotNone(conn)
        self.assertIsNotNone(meta)


if __name__ == '__main__':
    unittest.main()
