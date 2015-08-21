"""frameio
A Python Wrapper for the [Frame.io](http://www.frameio.com) API.
"""

import os
import requests

class FrameIO():
    def __init__(self):
        """
        :return:
        """

        self.email = None
        self.action_key = None
        self.messages = None
        self.errors = None

    def __str__(self):
        output = """FrameIO()
            self.email = %s
            self.action_key = %s
            self.messages = %s
            self.errors = %s
        """ % (self.email, self.action_key, self.messages, self.errors)

        return output

    def login(self, email, password=None):
        """Logs in to Frame.io
        Return True if successful, False if not"""

        #Email Check
        self.check_eligible(email=email)

        #Crap out if something goes wrong
        if self.errors:
            print self.errors
            return False

        print self

        #GoogleOAuth
        #Sign In
        #Sign Up


    def check_eligible(self, email=None):
        """Check to see if email address is valid. If it is, store it in the class.
        :return: Bool

        reference: http://docs.frameio.apiary.io/#reference/authentication/initial-mail-check/initial-mail-check
        """


        if not email:
            return False

        #Store the provided email in the class
        self.email = email

        #Check in w/ frame.io to see if this email is valid for login
        values = {
            "email": email
        }

        r = requests.post("https://api.frame.io/users/check_elegible", values)
        response = r.json()

        if "action_key" in response:
            self.action_key = response["action_key"]

        if "messages" in response:
            self.messages = response["messages"]

        if "errors" in response:
            self.errors = response["errors"]