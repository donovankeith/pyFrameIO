"""frameio_test
A simple script for testing the implementation of the Frame.io python wrapper."""

import unittest
import frameio

email = "tester@example.com"
password = "testing"

class LoginTestCase(unittest.TestCase):
    """Tests for `frameio.py`."""

    def test_good_email_and_pass(self):
        frameio_api = frameio.FrameIO()
        self.assertTrue(frameio_api.login(email=email, password=password))

    def test_good_email_and_bad_pass(self):
        frameio_api = frameio.FrameIO()
        self.assertFalse(frameio_api.login(email=email, password="sldfj"))

if __name__ == '__main__':
    unittest.main()