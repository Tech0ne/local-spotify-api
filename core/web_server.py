##############
#
#     @
#       @
#   @ @ @
#
##############


import sys

from flask import Flask
from flask_restx import Api

from .backends import DBusSpotifyAPIBackend
from .db import set_valid_users
from .meta_api import meta_api
from .player_api import player_api
from .status_api import status_api
from .web_server_utils import (error_model, get_backend, normal_model,
                               set_backend, disable_authentication)

AVAILABLE_BACKENDS = {"dbus": DBusSpotifyAPIBackend}


authorizations = {
    "basic": {
        "type": "basic",
        "description": "Enter username and password",
    }
}


def make_app(uses_auth: bool, creds: dict, backend_name: str, version: str):
    app = Flask(__name__)
    if uses_auth:
        api = Api(
            app,
            version=version,
            title="Spotify API",
            description="Interact with running Spotify Instance through Web \
API. Locked with basic auth",
            authorizations=authorizations,
            security="basicAuth",
        )

        set_valid_users(creds)
    else:
        api = Api(
            app,
            version=version,
            title="Spotify API",
            description="Interact with running Spotify Instance through Web \
API.",
        )

        disable_authentication()

    api.add_model("Ok", normal_model)
    api.add_model("Error", error_model)
    api.add_namespace(meta_api)
    api.add_namespace(player_api)
    api.add_namespace(status_api)

    set_backend(AVAILABLE_BACKENDS.get(backend_name)())

    if get_backend() is None:
        print(f'Backend "{backend_name}" not found !', file=sys.stderr)
        sys.exit(1)

    return app
