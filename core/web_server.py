import base64
import sys

from flask import Flask, request
from flask_restx import Api, Namespace, Resource, fields, reqparse

from .backends import DBusSpotifyAPIBackend

AVAILABLE_BACKENDS = {"dbus": DBusSpotifyAPIBackend}


authorizations = {
    "basic": {
        "type": "basic",
        "description": "Enter username and password",
    }
}

VALID_USERS = {}

backend = None


def check_basic_auth(auth_header):
    if not auth_header or not auth_header.startswith("Basic "):
        return False

    encoded_credentials = auth_header.split(" ")[1]
    try:
        decoded = base64.b64decode(encoded_credentials).decode("utf-8")
        username, password = decoded.split(":")
        return VALID_USERS.get(username) == password
    except Exception:
        return False


def basic_auth_required(func):
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization")
        if not check_basic_auth(auth):
            return {"message": "Unauthorized"}, 401
        return func(*args, **kwargs)

    return wrapper


# Player API #

player_api = Namespace(
    "Player API",
    description="Interact with the actual player. Play, Pause, Stop...",
    path="/api/player",
)


@player_api.route("/play")
class Play(Resource):
    @player_api.doc(security="basic")
    @basic_auth_required
    def post(self):
        if backend is None:
            return {"status": False, "error": "backend is None"}
        return backend.play()


@player_api.route("/pause")
class Pause(Resource):
    @player_api.doc(security="basic")
    @basic_auth_required
    def post(self):
        if backend is None:
            return {"status": False, "error": "backend is None"}
        return backend.pause()


@player_api.route("/playpause")
class PlayPause(Resource):
    @player_api.doc(security="basic")
    @basic_auth_required
    def post(self):
        if backend is None:
            return {"status": False, "error": "backend is None"}
        return backend.toggle_play_pause()


@player_api.route("/stop")
class Stop(Resource):
    @player_api.doc(security="basic")
    @basic_auth_required
    def post(self):
        if backend is None:
            return {"status": False, "error": "backend is None"}
        return backend.stop()


@player_api.route("/next")
class Next(Resource):
    @player_api.doc(security="basic")
    @basic_auth_required
    def post(self):
        if backend is None:
            return {"status": False, "error": "backend is None"}
        return backend.skip()


@player_api.route("/prev")
class Prev(Resource):
    @player_api.doc(security="basic")
    @basic_auth_required
    def post(self):
        if backend is None:
            return {"status": False, "error": "backend is None"}
        return backend.prev()


seek_model = player_api.model(
    "Seek",
    {
        "seconds": fields.Integer(
            required=True,
            description="Seek amount. Negative for backward seek",
        )
    },
)


@player_api.route("/seek")
class Seek(Resource):
    @player_api.doc(security="basic")
    @player_api.expect(seek_model)
    @basic_auth_required
    def post(self):
        if backend is None:
            return {"status": False, "error": "backend is None"}

        parser = reqparse.RequestParser()
        parser.add_argument(
            "seconds",
            type=int,
            help="Seconds to seek. \
Negative to seek backward",
        )
        args = parser.parse_args()

        return backend.seek(args.get("seconds"))


# /Player API #
# Meta API #


meta_api = Namespace(
    "Meta API",
    description="API interacting with the global state of the Spotify App",
    path="/api/meta",
)


@meta_api.route("/show")
class Show(Resource):
    @meta_api.doc(security="basic")
    @basic_auth_required
    def post(self):
        if backend is None:
            return {"status": False, "error": "backend is None"}
        return backend.show()


@meta_api.route("/current")
class CurrentSong(Resource):
    @meta_api.doc(security="basic")
    @basic_auth_required
    def get(self):
        if backend is None:
            return {"status": False, "error": "backend is None"}
        return backend.get_current_song()


@meta_api.route("/playing")
class Playing(Resource):
    @meta_api.doc(security="basic")
    @basic_auth_required
    def get(self):
        if backend is None:
            return {"status": False, "error": "backend is None"}
        return backend.get_playing()


# /Meta API #
# Status API #

status_api = Namespace(
    "Status API",
    description="API used to interact with global states of Spotify Client, \
like current playing position, volume...",
    path="/api/status",
)


position_model = status_api.model(
    "Position",
    {
        "seconds": fields.Integer(
            required=True,
            description="New position of the current track",
        )
    },
)


@status_api.route("/position")
class Position(Resource):
    @meta_api.doc(security="basic")
    @basic_auth_required
    def get(self):
        if backend is None:
            return {"status": False, "error": "backend is None"}
        return backend.get_position()

    @meta_api.doc(security="basic")
    @basic_auth_required
    def post(self):
        if backend is None:
            return {"status": False, "error": "backend is None"}

        parser = reqparse.RequestParser()
        parser.add_argument(
            "seconds",
            type=int,
            help="New position of the \
current track",
        )
        args = parser.parse_args()

        return backend.set_position(args.get("seconds"))


def loop_value(loop: str):
    value = loop.capitalize()
    if value == "None" or value == "Playlist" or value == "Track":
        return value
    raise TypeError(
        f'Could not parse "{loop}" as one of "None", \
"Playlist" or "Track"'
    )


loop_model = status_api.model(
    "Loop",
    {
        "loop": fields.String(
            required=True,
            description="Disable loop, set playlist loop or track loop, \
respectively",
            enum=["None", "Playlist", "Track"],
        )
    },
)


@status_api.route("/loop")
class Loop(Resource):
    @meta_api.doc(security="basic")
    @basic_auth_required
    def get(self):
        if backend is None:
            return {"status": False, "error": "backend is None"}
        return backend.get_loop()

    @meta_api.doc(security="basic")
    @meta_api.expect(loop_model)
    @basic_auth_required
    def post(self):
        if backend is None:
            return {"status": False, "error": "backend is None"}

        parser = reqparse.RequestParser()
        parser.add_argument(
            "loop",
            type=loop_value,
            help="Disable loop, set playlist loop or track loop.",
        )
        args = parser.parse_args()

        return backend.set_loop(args.get("loop"))


shuffle_model = status_api.model(
    "Shuffle",
    {
        "shuffle": fields.Boolean(
            required=True,
            description="Disable loop, set playlist loop or track loop, \
respectively",
        )
    },
)


@status_api.route("/shuffle")
class Shuffle(Resource):
    @meta_api.doc(security="basic")
    @basic_auth_required
    def get(self):
        if backend is None:
            return {"status": False, "error": "backend is None"}
        return backend.get_shuffle()

    @meta_api.doc(security="basic")
    @meta_api.expect(shuffle_model)
    @basic_auth_required
    def post(self):
        if backend is None:
            return {"status": False, "error": "backend is None"}

        parser = reqparse.RequestParser()
        parser.add_argument(
            "shuffle",
            type=bool,
            help="Enable / Disable shuffle mode. No effect on \
\"Smart Shuffle\" functionality",
        )
        args = parser.parse_args()

        return backend.set_shuffle(args.get("shuffle"))


def volume_value(volume: float):
    if volume > 1.0:
        return 1.0
    if volume < 0.0:
        return 0.0
    return volume


volume_model = status_api.model(
    "Volume",
    {
        "volume": fields.Float(
            required=True,
            description="Set volume. Must be between 0.0 and 1.0",
        )
    },
)


@status_api.route("/volume")
class Volume(Resource):
    @meta_api.doc(security="basic")
    @basic_auth_required
    def get(self):
        if backend is None:
            return {"status": False, "error": "backend is None"}
        return backend.get_volume()

    @meta_api.doc(security="basic")
    @meta_api.expect(volume_model)
    @basic_auth_required
    def post(self):
        if backend is None:
            return {"status": False, "error": "backend is None"}

        parser = reqparse.RequestParser()
        parser.add_argument(
            "volume",
            type=volume_value,
            help="Set volume. Must be between 0.0 and 1.0",
        )
        args = parser.parse_args()

        return backend.set_volume(args.get("volume"))


# /Status API #


def make_app(uses_auth: bool, creds: dict, backend_name: str, version: str):
    global backend, check_basic_auth, VALID_USERS

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

        VALID_USERS = creds
    else:
        api = Api(
            app,
            version=version,
            title="Spotify API",
            description="Interact with running Spotify Instance through Web \
API.",
        )

        def check_basic_auth(_):
            return True  # bypass authentication

    api.add_namespace(meta_api)
    api.add_namespace(player_api)
    api.add_namespace(status_api)

    backend = AVAILABLE_BACKENDS.get(backend_name)()

    if backend is None:
        print(f'Backend "{backend_name}" not found !', file=sys.stderr)
        sys.exit(1)

    return app
