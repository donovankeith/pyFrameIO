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

    def __str__(self):
        output = """FrameIO()
            self.email = %s
            self.action_key = %s
            self.messages = %s
            self.errors = %s
            self.user_id = %s
            self.token = %s
        """ % (self.email, self.action_key, self.messages, self.errors, self.user_id, self.token)

        return output

    def login(self, email, password=None):
        """Logs in to Frame.io
        Return True if successful, False if not"""

        #Email Check
        if not self.check_eligible(email=email):
            return False

        self.password = password

        #Crap out if something goes wrong
        if self.errors:
            print self.errors
            return False

        if not self.action_key:
            print "No action key, don't know how to login"
            return False

        print "password: ", self.password
        print self

        if self.action_key == "user-non-google":
            print "Non-Google User, standard login okay"
            return self.login_user_non_google()

        elif self.action_key == "user-google":
            print "Google Login"
            #TODO: Implement
        elif self.action_key == "user-eligible":
            print "Eligible for sign-up"
            #TODO: Implement
        else:
            print "Non-implemented action_key: ", self.action_key

    def login_user_non_google(self):
        """Login the user w/ the stored credentials.
        Return True if successful, False if any errors."""

        values = {
            "a": self.email,
            "b": self.password
        }

        r = requests.post("https://api.frame.io/login", values)
        response = r.json()

        print response

        if "x" in response:
            self.user_id = response["x"]

        if "y" in response:
            self.token = response["y"]

        if "messages" in response:
            self.messages = response["messages"]

        if "errors" in response:
            self.errors = response["errors"]
            print self.errors
            return False

        return True

    def check_eligible(self, email=None):
        """Check to see if email address is valid. If it is, store it in the class.

        reference: http://docs.frameio.apiary.io/#reference/authentication/initial-mail-check/initial-mail-check

        return True if eligible, False if not.
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

        if not self.errors:
            return True
        else:
            return False