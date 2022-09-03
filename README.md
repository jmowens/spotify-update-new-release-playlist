# spotify-update-new-release-playlist

The purpose of this script is to update a playlist with new album releases from followed artists.

## How to Use

It is assumed you have:

- A Spotify account
- Some artists you are following
- A playlist that you want this script to update
- [Spotify API access](https://developer.spotify.com/)

You will need to create a Python environment to run the script in. You can use [poetry](https://python-poetry.org/docs/) with the project's toml file. The only dependency is [tekore](https://tekore.readthedocs.io/en/stable/index.html) so it should be easy to manually setup an environment.

In whatever directory you run the script from, create a `settings.cfg` file to store a few pieces of information:

```
[DEFAULT]
earliest_release_date = YYYY-MM-DD

[SPOTIFY]
client_id = <get this from your Spotify API access dashboard>
client_secret = <get this from your Spotify API access dashboard>
redirect_uri = <get this from your Spotify API access dashboard under Edit Settings>
playlist_id = <if you copy a link to your playlist it is the value after the last / and before the ?>
```

On your first run you probably don't want to add every album from every artist you follow. Set the `earliest_release_date` to whatever is appropriate and only albums released after that date will be added to your playlist.

When the script finishes running it updates `earliest_release_date` to the current date so that subsequent runs of the script will not add the same albums.

On the first run a browser window should open for authorization. Allow access and your browser should be redirected. Copy the URL and paste it into the console where the script is running. Do this even if the redirect page is not successfully loaded (e.g., it is a localhost). The script will create a `tekore.cfg` file to manage authorizations going forward.

The script will print out the albums it added to the playlist.