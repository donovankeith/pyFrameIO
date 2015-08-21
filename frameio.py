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

        print response

        action_key = None
        messages = None
        errors = None

        if "action_key" in response:
            action_key = response["action_key"]

        if "messages" in response:
            messages = response["messages"]

        if "errors" in response:
            errors = response["errors"]

        print "action_key: ", action_key
        print "messages: ", messages
        print "errors: ", errors