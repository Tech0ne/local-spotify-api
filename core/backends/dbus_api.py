##############
#
#     @
#       @
#   @ @ @
#
##############

import dbus
from .backend import SpotifyAPIBackend


class DBusSpotifyAPIBackend(SpotifyAPIBackend):
    def __init__(self):
        self.dbus = dbus.SessionBus()
        self.proxy = self.dbus.get_object(
            "org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2"
        )
        self.root_interface = dbus.Interface(
            self.proxy, dbus_interface="org.mpris.MediaPlayer2"
        )
        self.player_interface = dbus.Interface(
            self.proxy, dbus_interface="org.mpris.MediaPlayer2.Player"
        )
        self.properties_interface = dbus.Interface(
            self.proxy, dbus_interface="org.freedesktop.DBus.Properties"
        )
        super().__init__()

    def _get_normalised_value(self, value):
        if isinstance(value, dbus.Dictionary):
            return {
                self._get_normalised_value(k): self._get_normalised_value(v)
                for k, v in value.items()
            }
        elif isinstance(value, dbus.Array):
            return [self._get_normalised_value(v) for v in value]
        elif isinstance(value, (dbus.String, dbus.ObjectPath)):
            return str(value)
        elif isinstance(
            value,
            (
                dbus.Int64,
                dbus.Int32,
                dbus.Int16,
                dbus.Byte,
                dbus.UInt64,
                dbus.UInt32,
                dbus.UInt16,
            ),
        ):
            return int(value)
        elif isinstance(value, dbus.Boolean):
            return bool(value)
        elif isinstance(value, dbus.Double):
            return float(value)
        return value

    def get_current_metadata(self) -> dict:
        return self._get_normalised_value(
            self.properties_interface.Get(
                "org.mpris.MediaPlayer2.Player",
                "Metadata",
            )
        )

    def play(self) -> dict:
        try:
            self.player_interface.Play()
        except dbus.DBusException as e:
            return {"status": False, "error": str(e)}
        return {"status": True}

    def pause(self) -> dict:
        try:
            self.player_interface.Pause()
        except dbus.DBusException as e:
            return {"status": False, "error": str(e)}
        return {"status": True}

    def toggle_play_pause(self) -> dict:
        try:
            self.player_interface.PlayPause()
        except dbus.DBusException as e:
            return {"status": False, "error": str(e)}
        return {"status": True}

    def stop(self) -> dict:
        try:
            self.player_interface.Stop()
            self.root_interface.Quit()
        except dbus.DBusException as e:
            return {"status": False, "error": str(e)}
        return {"status": True}

    def show(self) -> dict:
        try:
            self.root_interface.Raise()
        except dbus.DBusException as e:
            return {"status": False, "error": str(e)}
        return {"status": True}

    def skip(self) -> dict:
        try:
            if not self._get_normalised_value(
                self.properties_interface.Get(
                    "org.mpris.MediaPlayer2.Player",
                    "CanGoNext",
                )
            ):
                return {"status": False, "error": "can not next"}
            self.player_interface.Next()
        except dbus.DBusException as e:
            return {"status": False, "error": str(e)}
        return {"status": True}

    def prev(self) -> dict:
        try:
            if not self._get_normalised_value(
                self.properties_interface.Get(
                    "org.mpris.MediaPlayer2.Player",
                    "CanGoPrevious",
                )
            ):
                return {"status": False, "error": "can not previous"}
            self.player_interface.Previous()
        except dbus.DBusException as e:
            return {"status": False, "error": str(e)}
        return {"status": True}

    def seek(self, seconds: int) -> dict:
        try:
            if not self._get_normalised_value(
                self.properties_interface.Get(
                    "org.mpris.MediaPlayer2.Player",
                    "CanSeek",
                )
            ):
                return {"status": False, "error": "can not seek"}
            self.player_interface.Seek(dbus.Int64(seconds * 1_000_000))
        except dbus.DBusException as e:
            return {"status": False, "error": str(e)}
        return {"status": True}

    def set_position(self, seconds: int) -> dict:
        try:
            metadata = self.get_current_metadata()

            self.player_interface.SetPosition(
                dbus.ObjectPath(metadata.get("mpris:trackid")),
                dbus.Int64(seconds * 1_000_000),
            )
        except dbus.DBusException as e:
            return {"status": False, "error": str(e)}
        return {"status": True}

    def get_position(self) -> dict:
        try:
            position = self._get_normalised_value(
                self.properties_interface.Get(
                    "org.mpris.MediaPlayer2.Player",
                    "Position",
                )
            )
        except dbus.DBusException as e:
            return {"status": False, "error": str(e)}
        return {"status": True, "position": position}

    def set_loop(self, loop_status: str) -> dict:
        if loop_status is None:
            return {"status": False, "error": "missing input value"}
        try:
            self.properties_interface.Set(
                "org.mpris.MediaPlayer2.Player",
                "LoopStatus",
                dbus.String(loop_status),  # "None", "Playlist" or "Track"
            )
        except dbus.DBusException as e:
            return {"status": False, "error": str(e)}
        return {"status": True}

    def get_loop(self) -> dict:
        try:
            loop = self._get_normalised_value(
                self.properties_interface.Get(
                    "org.mpris.MediaPlayer2.Player",
                    "LoopStatus",
                )
            )
        except dbus.DBusException as e:
            return {"status": False, "error": str(e)}
        return {"status": True, "loop": loop}

    def set_shuffle(self, shuffle: bool) -> dict:
        try:
            self.properties_interface.Set(
                "org.mpris.MediaPlayer2.Player",
                "Shuffle",
                dbus.Boolean(shuffle),
            )
        except dbus.DBusException as e:
            return {"status": False, "error": str(e)}
        return {"status": True}

    def get_shuffle(self) -> dict:
        try:
            shuffle = self._get_normalised_value(
                self.properties_interface.Get(
                    "org.mpris.MediaPlayer2.Player",
                    "Shuffle",
                )
            )
        except dbus.DBusException as e:
            return {"status": False, "error": str(e)}
        return {"status": True, "shuffle": shuffle}

    def set_volume(self, volume: float) -> dict:
        try:
            self.properties_interface.Set(
                "org.mpris.MediaPlayer2.Player",
                "Volume",
                dbus.Double(volume),
            )
        except dbus.DBusException as e:
            return {"status": False, "error": str(e)}
        return {"status": True}

    def get_volume(self) -> dict:
        try:
            volume = self._get_normalised_value(
                self.properties_interface.Get(
                    "org.mpris.MediaPlayer2.Player",
                    "Volume",
                )
            )
        except dbus.DBusException as e:
            return {"status": False, "error": str(e)}
        return {"status": True, "volume": volume}

    def get_current_song(self) -> dict:
        try:
            metadata = self.get_current_metadata()
        except dbus.DBusException as e:
            return {"status": False, "error": str(e)}
        return {
            "status": True,
            "current_song": {k.split(":")[-1]: v for k, v in metadata.items()},
        }

    def get_playing(self) -> dict:
        try:
            playing = self._get_normalised_value(
                self.properties_interface.Get(
                    "org.mpris.MediaPlayer2.Player",
                    "PlaybackStatus",
                )
            )
        except dbus.DBusException as e:
            return {"status": False, "error": str(e)}
        return {"status": True, "playing": playing}
