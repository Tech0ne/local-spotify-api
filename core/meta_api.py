from flask_restx import Namespace, Resource

from .web_server_utils import (basic_auth_required, error_model,
                               formated_output, get_backend, normal_model)

meta_api = Namespace(
    "Meta API",
    description="API interacting with the global state of the Spotify App",
    path="/api/meta",
)


@meta_api.route("/show")
class Show(Resource):
    @meta_api.doc(security="basic")
    @meta_api.response(200, "Ok", normal_model)
    @meta_api.response(500, "Error", error_model)
    @basic_auth_required
    def post(self):
        if get_backend() is None:
            return {"status": False, "error": "backend is None"}
        return formated_output(get_backend().show())


@meta_api.route("/current")
class CurrentSong(Resource):
    @meta_api.doc(security="basic")
    @meta_api.response(500, "Error", error_model)
    @basic_auth_required
    def get(self):
        if get_backend() is None:
            return {"status": False, "error": "backend is None"}
        return formated_output(get_backend().get_current_song())


@meta_api.route("/playing")
class Playing(Resource):
    @meta_api.doc(security="basic")
    @meta_api.response(500, "Error", error_model)
    @basic_auth_required
    def get(self):
        if get_backend() is None:
            return {"status": False, "error": "backend is None"}
        return formated_output(get_backend().get_playing())


@meta_api.route("/sync")
class Sync(Resource):
    @meta_api.doc(security="basic")
    @meta_api.response(200, "Ok", normal_model)
    @meta_api.response(500, "Error", error_model)
    @basic_auth_required
    def post(self):
        if get_backend() is None:
            return {"status": False, "error": "backend is None"}
        return formated_output(get_backend().resync())
