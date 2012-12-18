import os
from mock import Mock
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from gomusic import GoMusicManager

class TestGoMusic(unittest.TestCase):
    def test_init_1(self):
        self.assertRaises(TypeError, GoMusicManager, None)

    def test_init_2(self):
        gmm = GoMusicManager('email', 'pw', 'id')
        self.assertTrue(isinstance(gmm, GoMusicManager))

    def test_init_3(self):
        gmm = GoMusicManager('email', 'pw', 'id', debug=1)
        self.assertTrue(isinstance(gmm, GoMusicManager))

    def test_login_data(self):
        email = '123@456'
        password = 'password'
        gmm = GoMusicManager(email, password, 'id')
        gmm._request = Mock()
        gmm._response = Mock()
        gmm._validate_request = Mock()
        gmm.login()
        data = {'login': email, 'password': password,
                'remember': 'on', 'submit': 'login'}
        url = 'http://www.gomusicnow.com/login.html'
        gmm._request.assert_called_once_with(url, data)
        gmm._validate_request.assert_called_once_with()

    def test_login_good(self):
        email = '123@456'
        password = 'password'
        gmm = GoMusicManager(email, password, 'id')
        gmm._request = Mock()
        gmm._validate_request = Mock()
        gmm._validate_request.return_value = True
        res = gmm.login()
        self.assertEqual(gmm.login(), True)

    def test_login_bad(self):
        email = '123@456'
        password = 'password'
        gmm = GoMusicManager(email, password, 'id')
        gmm._request = Mock()
        gmm._validate_request = Mock()
        gmm._validate_request.return_value = False
        res = gmm.login()
        self.assertEqual(gmm.login(), False)

if __name__ == '__main__':
    unittest.main()
