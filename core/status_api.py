from flask_restx import Namespace, Resource, fields, reqparse

from .web_server_utils import (basic_auth_required, error_model,
                               formated_output, get_backend, normal_model)

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
    @status_api.doc(security="basic")
    @status_api.response(500, "Error", error_model)
    @basic_auth_required
    def get(self):
        if get_backend() is None:
            return {"status": False, "error": "backend is None"}
        return formated_output(get_backend().get_position())

    @status_api.doc(security="basic")
    @status_api.response(200, "Ok", normal_model)
    @status_api.response(500, "Error", error_model)
    @status_api.expect(position_model)
    @basic_auth_required
    def post(self):
        if get_backend() is None:
            return {"status": False, "error": "backend is None"}

        parser = reqparse.RequestParser()
        parser.add_argument(
            "seconds",
            type=int,
            help="New position of the \
current track",
        )
        args = parser.parse_args()

        return formated_output(get_backend().set_position(args.get("seconds")))


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
    @status_api.doc(security="basic")
    @status_api.response(500, "Error", error_model)
    @basic_auth_required
    def get(self):
        if get_backend() is None:
            return {"status": False, "error": "backend is None"}
        return formated_output(get_backend().get_loop())

    @status_api.doc(security="basic")
    @status_api.response(200, "Ok", normal_model)
    @status_api.response(500, "Error", error_model)
    @status_api.expect(loop_model)
    @basic_auth_required
    def post(self):
        if get_backend() is None:
            return {"status": False, "error": "backend is None"}

        parser = reqparse.RequestParser()
        parser.add_argument(
            "loop",
            type=loop_value,
            help="Disable loop, set playlist loop or track loop.",
        )
        args = parser.parse_args()

        return formated_output(get_backend().set_loop(args.get("loop")))


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
    @status_api.doc(security="basic")
    @status_api.response(500, "Error", error_model)
    @basic_auth_required
    def get(self):
        if get_backend() is None:
            return {"status": False, "error": "backend is None"}
        return formated_output(get_backend().get_shuffle())

    @status_api.doc(security="basic")
    @status_api.response(200, "Ok", normal_model)
    @status_api.response(500, "Error", error_model)
    @status_api.expect(shuffle_model)
    @basic_auth_required
    def post(self):
        if get_backend() is None:
            return {"status": False, "error": "backend is None"}

        parser = reqparse.RequestParser()
        parser.add_argument(
            "shuffle",
            type=bool,
            help='Enable / Disable shuffle mode. No effect on \
"Smart Shuffle" functionality',
        )
        args = parser.parse_args()

        return formated_output(get_backend().set_shuffle(args.get("shuffle")))


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
    @status_api.doc(security="basic")
    @status_api.response(500, "Error", error_model)
    @basic_auth_required
    def get(self):
        if get_backend() is None:
            return {"status": False, "error": "backend is None"}
        return formated_output(get_backend().get_volume())

    @status_api.doc(security="basic")
    @status_api.response(200, "Ok", normal_model)
    @status_api.response(500, "Error", error_model)
    @status_api.expect(volume_model)
    @basic_auth_required
    def post(self):
        if get_backend() is None:
            return {"status": False, "error": "backend is None"}

        parser = reqparse.RequestParser()
        parser.add_argument(
            "volume",
            type=volume_value,
            help="Set volume. Must be between 0.0 and 1.0",
        )
        args = parser.parse_args()

        return formated_output(get_backend().set_volume(args.get("volume")))
