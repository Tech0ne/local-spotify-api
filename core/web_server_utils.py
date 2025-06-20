import base64

from flask import request
from flask_restx import Model, fields

from .backends import SpotifyAPIBackend
from .db import get_valid_users

BACKEND = None

normal_model = Model(
    "Ok",
    {
        "status": fields.Boolean(
            description="Status of the executed action",
            default=True,
        )
    },
)

error_model = Model(
    "Error",
    {
        "status": fields.Boolean(
            description="Status of the executed action",
            default=False,
        ),
        "error": fields.String(
            description="Detail of the error that happened",
        ),
    },
)


def check_basic_auth(auth_header):
    if not auth_header or not auth_header.startswith("Basic "):
        return False

    encoded_credentials = auth_header.split(" ")[1]
    try:
        decoded = base64.b64decode(encoded_credentials).decode("utf-8")
        username, password = decoded.split(":")
        return get_valid_users().get(username) == password
    except Exception:
        return False


def basic_auth_required(func):
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization")
        if not check_basic_auth(auth):
            return {"message": "Unauthorized"}, 401
        return func(*args, **kwargs)

    return wrapper


def formated_output(output: dict):
    error_code = (
        200
        if output.get("status")
        else output.get(
            "http_status_code",
            500,
        )
    )
    if output.get("http_status_code") is not None:
        output.pop("http_status_code")
    return (output, error_code)


def disable_authentication():
    global check_basic_auth

    def check_basic_auth(_):
        return True # Bypass authentication


def get_backend():
    return BACKEND


def set_backend(backend: SpotifyAPIBackend):
    global BACKEND
    BACKEND = backend
