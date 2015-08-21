"""frameio_test
A simple script for testing the implementation of the Frame.io python wrapper."""

import frameio

#globals
email = "tester@example.com"
password = "testing"

def main():
    frameio_api = frameio.FrameIO()
    frameio_api.login(email)

if __name__ == "__main__":
    main()