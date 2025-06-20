# local-spotify-api
Allows you to interact with spotify with a web API.

## What does it solve ?

Do you want to integrate spotify with any other tool ?

Well, you can't because of recent decisions, removing the web based API.

This tool "fixes" that by interacting with still present APIs to merge into web based API.

Secured through simple Basic HTTP Auth, you can now controle the music from anything.

## How does it work ?

There are multiple "backends".

The idea is that a "backend" is just a "raw" Spotify API.

You can make your own too !

Copy the `core/backends/backend.py` to have the base.

Your new class must inherite from `SpotifyAPIBackend`.

Check out `core/backends/dbus_api.py` for some inspiration.

## How can I configure it ?

Edit the `main.py` file.

You can change:

- `USES_AUTHENTICATION`: define the behaviour of the server. if set to `True`, you'll need to authenticate with a valid user:password combination.
- `USERS`: define the users that can authenticate.
- `BACKEND`: define the used backend. Note: for now, only `dbus` is available. You can add more on the `core/backends/` directory, and by adding them to the `AVAILABLE_BACKENDS` variable, found on the `core/web_server.py` file.
- `VERSION`: version number shown on swagger

# Support

- [x] Linux
  - using dbus
- [ ] MacOS (ongoing)
  - using applescript
- [ ] Windows (not planned for now)
