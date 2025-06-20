from core import make_app

USES_AUTHENTICATION = False
USERS = {
    "user": "password"
}

BACKEND = "dbus"

VERSION = "1.0"

if __name__ == "__main__":
    app = make_app(USES_AUTHENTICATION, USERS, BACKEND, VERSION)
    try:
        app.run(host="0.0.0.0", port=80)
    except SystemExit:
        app.run(host="0.0.0.0", port=8080)
