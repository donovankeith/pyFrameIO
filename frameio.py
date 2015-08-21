"""frameio
A Python Wrapper for the [Frame.io](http://www.frameio.com) API.
"""

import os
import requests

class FrameIO():
    def __init__(self):
        """Create a new FrameIO object
        """

        #Minimum info provided by user
        self.email = None
        self.password = None

        #Responses from check_eligible
        self.action_key = None
        self.messages = None
        self.errors = None

        #Responses from login
        self.user_id = None
        self.token = None

    def check_eligible(self, email):
        """Check to see if email address is valid. Store response in class.
        returns True if successful, False if not.

        reference:
        http://docs.frameio.apiary.io/#reference/authentication/initial-mail-check/initial-mail-check
        """

        #Check in w/ frame.io to see if this email is valid for login
        values = {
            "email": email
        }

        r = requests.post("https://api.frame.io/users/check_elegible", values)
        response = r.json()

        self.messages = response.get("messages")
        self.action_key = response.get("action_key")

        errors = response.get("errors")
        if errors:
            print errors
            return False

        return True

    def login(self, email, password):
        """Logs in to Frame.io w/ email & password pair
        returns True if successful, False if not

        reference:
        http://docs.frameio.apiary.io/#reference/authentication/login-with-frameio-account/login-with-frame.io-account
        """

        #Email Check
        if not self.check_eligible(email=email):
            return False

        #Try to login
        values = {
            "a": email,
            "b": password
        }

        r = requests.post("https://api.frame.io/login", values)
        response = r.json()

        #Bail if something went wrong
        errors = response.get("errors")
        if errors:
            print errors
            return False

        #Must have worked
        #Store the login info
        self.email = email
        self.password = password

        #And the response
        self.user_id = response.get("x")
        self.token = response.get("y")
        self.messages = response.get("messages")

        return True