import requests
from bs4 import BeautifulSoup
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth


SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
SPOTIFY_REDIRECT_URI = "https://example.com/"


date = input("What date would you like to compile from?\nInput date as YYYY-MM-DD:\n")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
billboard_webpage = response.text

soup = BeautifulSoup(billboard_webpage, "html.parser")

song_class = "c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-" \
             "u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 " \
             "u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only"

songs = soup.find_all(name="h3", id="title-of-a-story", class_=song_class)
song_list = [song.getText().strip("\n") for song in songs]


# Authenticate with Spotify

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        show_dialog=True,
        cache_path="token.txt",
    )
)
user_id = sp.current_user()["id"]


# Search Spotify for songs, create list of Spotify song URIs for songs in song_list

uri_list = []

for song in song_list:
    song_search = sp.search(q=f"track:{song}", type="track")
    try:
        print(song_search["tracks"]["items"][0]["name"])
        uri = song_search["tracks"]["items"][0]["uri"]
    except IndexError:
        print(f"{song} doesn't exist in Spotify... skipped")
    else:
        uri_list.append(uri)

playlist = sp.user_playlist_create(
    user=user_id,
    name=f"{date} Billboard 100",
    public=False,
    description=f"A playlist created from the top 100 songs on the day of {date}"
)

print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=uri_list)

