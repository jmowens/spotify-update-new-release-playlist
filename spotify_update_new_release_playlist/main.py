import os
from configparser import ConfigParser
from datetime import datetime, timezone

import tekore as tk

SETTINGS_CONFIG_FILE_NAME = "settings.cfg"
TEKORE_CONFIG_FILENAME = "tekore.cfg"
SPOTIFY_SCOPE = (
    tk.scope.user_follow_read
    + tk.scope.playlist_modify_private
    + tk.scope.playlist_modify_public
)


def main():
    settings_config = settings_config_from_file()
    earliest_release_date = settings_config["DEFAULT"]["EARLIEST_RELEASE_DATE"]
    earliest_release_date = datetime.strptime(earliest_release_date, "%Y-%m-%d")
    playlist_id = settings_config["SPOTIFY"]["PLAYLIST_ID"]

    spotify = get_spotify_client(settings_config)
    for artist in spotify.all_items(spotify.followed_artists()):
        for album in spotify.all_items(spotify.artist_albums(artist.id, ["album"])):
            release_date = parse_date_string(album.release_date)
            if release_date >= earliest_release_date:
                track_uris = []
                for track in spotify.all_items(spotify.album_tracks(album.id)):
                    track_uris.append(track.uri)
                spotify.playlist_remove(playlist_id, track_uris)
                spotify.playlist_add(playlist_id, track_uris)
                print(f"{artist.name} - {album.name} - {album.release_date}")

    settings_config_to_file(settings_config)


def settings_config_from_file() -> ConfigParser:
    settings_config = ConfigParser()
    settings_config.read(SETTINGS_CONFIG_FILE_NAME)
    return settings_config


def settings_config_to_file(settings_config: ConfigParser) -> None:
    next_earliest_release_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    settings_config["DEFAULT"]["EARLIEST_RELEASE_DATE"] = next_earliest_release_date
    with open(SETTINGS_CONFIG_FILE_NAME, mode="w", encoding="utf8") as fp:
        settings_config.write(fp)


def get_spotify_client(settings_config: ConfigParser) -> tk.Spotify:
    if os.path.isfile(TEKORE_CONFIG_FILENAME):
        tekore_config = tk.config_from_file(TEKORE_CONFIG_FILENAME, return_refresh=True)
        user_token = tk.refresh_user_token(*tekore_config[:2], tekore_config[3])
    else:
        user_token = tk.prompt_for_user_token(
            settings_config["SPOTIFY"]["CLIENT_ID"],
            settings_config["SPOTIFY"]["CLIENT_SECRET"],
            settings_config["SPOTIFY"]["REDIRECT_URI"],
            scope=SPOTIFY_SCOPE,
        )
        tekore_config = (
            settings_config["SPOTIFY"]["CLIENT_ID"],
            settings_config["SPOTIFY"]["CLIENT_SECRET"],
            settings_config["SPOTIFY"]["REDIRECT_URI"],
            user_token.refresh_token,
        )
        tk.config_to_file(TEKORE_CONFIG_FILENAME, tekore_config)
    return tk.Spotify(user_token, max_limits_on=True, chunked_on=True)


def parse_date_string(date_string: str) -> datetime:
    try:
        return datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError:
        return datetime.strptime(date_string, "%Y")


if __name__ == "__main__":
    main()
