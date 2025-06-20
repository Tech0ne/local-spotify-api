##############
#
#     @
#       @
#   @ @ @
#
##############


class SpotifyAPIBackend:
    def __init__(self):
        pass

    # Every Output will either contain:
    #   {"status": False, "error": "description of the error"}
    # or
    #   {"status": True, [the described output]}

    # Input: None
    # Output: {}
    def play(self) -> dict:
        raise NotImplementedError("play is not implemented !")

    # Input: None
    # Output: {}
    def pause(self) -> dict:
        raise NotImplementedError("pause is not implemented !")

    # Input: None
    # Output: {}
    def toggle_play_pause(self) -> dict:
        raise NotImplementedError("toggle_play_pause is not implemented !")

    # Input: None
    # Output: {}
    def stop(self) -> dict:
        raise NotImplementedError("stop is not implemented !")

    # Input: None
    # Output: {}
    def show(self) -> dict:
        raise NotImplementedError("show is not implemented !")

    # Input: None
    # Output: {}
    def skip(self) -> dict:
        raise NotImplementedError("skip is not implemented !")

    # Input: None
    # Output: {}
    def prev(self) -> dict:
        raise NotImplementedError("prev is not implemented !")

    # Input: int
    # Output: {}
    def seek(self, seconds: int) -> dict:
        raise NotImplementedError("seek is not implemented !")

    # Input: int
    # Output: {}
    def set_position(self, seconds: int) -> dict:
        raise NotImplementedError("set_position is not implemented !")

    # Input: None
    # Output: {"position": int}
    def get_position(self) -> dict:
        raise NotImplementedError("get_position is not implemented !")

    # Input: "None" | "Playlist" | "Track"
    # Output: {}
    def set_loop(self, loop: str) -> dict:
        raise NotImplementedError("set_loop is not implemented !")

    # Input: None
    # Output: {"loop": "None" | "Playlist" | "Track"}
    def get_loop(self) -> dict:
        raise NotImplementedError("get_loop is not implemented !")

    # Input: bool
    # Output: {}
    def set_shuffle(self, shuffle: bool) -> dict:
        raise NotImplementedError("set_shuffle is not implemented !")

    # Input: None
    # Output: {"shuffle": bool}
    def get_shuffle(self) -> dict:
        raise NotImplementedError("get_shuffle is not implemented !")

    # Input: 0.0 - 1.0
    # Output: {}
    def set_volume(self, volume: float) -> dict:
        raise NotImplementedError("set_volume is not implemented !")

    # Input: None
    # Output: {"volume": 0.0 - 1.0}
    def get_volume(self, volume: float) -> dict:
        raise NotImplementedError("get_volume is not implemented !")

    # Input: None
    # Output: {"current_song": [output is implementation dependent]}
    def get_current_song(self) -> dict:
        raise NotImplementedError("get_current_song is not implemented !")

    # Input: int
    # Output: {"playing": bool}
    def get_playing(self) -> dict:
        raise NotImplementedError("get_playing is not implemented !")
