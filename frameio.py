"""frameio
A Python Wrapper for the [Frame.io](http://www.frameio.com) API.
"""

import os
import requests

class User():
    def __init__(self, user_data):
        """Creates a User object with "user_data" dict"""

        self.id = user_data.get("id")
        self.name = user_data.get("name")
        self.first_name = user_data.get("first_name")
        self.last_name = user_data.get("last_name")
        self.email_confirmed_data = user_data.get("email_confirmed_data")
        self.has_logged_in = user_data.get("has_logged_in")
        self.created_at_integer = user_data.get("created_at_integer")
        self.account_key = user_data.get("account_key")
        self.email = user_data.get("email")
        self.link = user_data.get("link")
        self.location = user_data.get("location")
        self.bio = user_data.get("bio")
        self.profile_image = user_data.get("profile_image") #URL of profile images
        self.role = user_data.get("role")
        self.teams = user_data.get("teams", [])
        self.shared_projects = user_data.get("shared_projects", [])

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
        self.token = None
        self.user_id = None

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

    def get_user_data(self):
        """Return the user's data as a Dict with the following keys
        """

        #We can't get the user's data without the user_id & token
        if (self.user_id is None) or (self.token is None):
            return

        values = {
            "mid": self.user_id,
            "t": self.token
            }

        r = requests.post("https://api.frame.io/users/%s/data" % (self.user_id), values)
        response = r.json()

        return response