#!/usr/bin/env python3

##############
#
#     @
#       @
#   @ @ @
#
##############


from core import make_app

HOST = "0.0.0.0"
PORT = 8080

USES_AUTHENTICATION = False
USERS = {"user": "password"}

BACKEND = "dbus"

VERSION = "1.0"

if __name__ == "__main__":
    app = make_app(USES_AUTHENTICATION, USERS, BACKEND, VERSION)
    app.run(host=HOST, port=PORT, debug=False)
