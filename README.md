# Spotify playlist generator
A fun project created during a python coding camp

## Creates spotify playlists based on the top 100 songs from an input date given by the user.
- User inputs date in format YYYY-MM-DD.
- Searches billboard.com for the top 100 songs for that date.
- Beautiful soup module to scrape song data from billboard.com
- Authenticates with Spotify.
- Checks songs from top 100 list, according to uri. 
- Skips if song is not on Spotify.
- Complies a playlist, named according to the input date.
