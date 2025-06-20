from flask_restx import Namespace, Resource, fields, reqparse

from .web_server_utils import (basic_auth_required, error_model,
                               formated_output, get_backend, normal_model)

player_api = Namespace(
    "Player API",
    description="Interact with the actual player. Play, Pause, Stop...",
    path="/api/player",
)


@player_api.route("/play")
class Play(Resource):
    @player_api.doc(security="basic")
    @player_api.response(200, "Ok", normal_model)
    @player_api.response(500, "Error", error_model)
    @basic_auth_required
    def post(self):
        if get_backend() is None:
            return {"status": False, "error": "backend is None"}
        return formated_output(get_backend().play())


@player_api.route("/pause")
class Pause(Resource):
    @player_api.doc(security="basic")
    @player_api.response(200, "Ok", normal_model)
    @player_api.response(500, "Error", error_model)
    @basic_auth_required
    def post(self):
        if get_backend() is None:
            return {"status": False, "error": "backend is None"}
        return formated_output(get_backend().pause())


@player_api.route("/playpause")
class PlayPause(Resource):
    @player_api.doc(security="basic")
    @player_api.response(200, "Ok", normal_model)
    @player_api.response(500, "Error", error_model)
    @basic_auth_required
    def post(self):
        if get_backend() is None:
            return {"status": False, "error": "backend is None"}
        return formated_output(get_backend().toggle_play_pause())


@player_api.route("/stop")
class Stop(Resource):
    @player_api.doc(security="basic")
    @player_api.response(200, "Ok", normal_model)
    @player_api.response(500, "Error", error_model)
    @basic_auth_required
    def post(self):
        if get_backend() is None:
            return {"status": False, "error": "backend is None"}
        return formated_output(get_backend().stop())


@player_api.route("/next")
class Next(Resource):
    @player_api.doc(security="basic")
    @player_api.response(200, "Ok", normal_model)
    @player_api.response(500, "Error", error_model)
    @basic_auth_required
    def post(self):
        if get_backend() is None:
            return {"status": False, "error": "backend is None"}
        return formated_output(get_backend().skip())


@player_api.route("/prev")
class Prev(Resource):
    @player_api.doc(security="basic")
    @player_api.response(200, "Ok", normal_model)
    @player_api.response(500, "Error", error_model)
    @basic_auth_required
    def post(self):
        if get_backend() is None:
            return {"status": False, "error": "backend is None"}
        return formated_output(get_backend().prev())


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
    @player_api.response(200, "Ok", normal_model)
    @player_api.response(500, "Error", error_model)
    @player_api.expect(seek_model)
    @basic_auth_required
    def post(self):
        if get_backend() is None:
            return {"status": False, "error": "backend is None"}

        parser = reqparse.RequestParser()
        parser.add_argument(
            "seconds",
            type=int,
            help="Seconds to seek. \
Negative to seek backward",
        )
        args = parser.parse_args()

        return formated_output(get_backend().seek(args.get("seconds")))
