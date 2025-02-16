import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = "your client id"
client_secret = "your client secret"

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get("https://www.billboard.com/charts/hot-100/" + date)

soup = BeautifulSoup(response.text, "html.parser")
titles_with_html = soup.find_all(name="h3", class_="u-letter-spacing-0021", id="title-of-a-story")
 
song_titles = [title.text.strip() for title in titles_with_html]

for n in song_titles:
    if n == 'Producer(s):':
        song_titles.remove(n)
for n2 in song_titles:
    if n2 == "Imprint/Promotion Label:":
        song_titles.remove(n2)
for n3 in song_titles:
    if n3 == 'Songwriter(s):':
        song_titles.remove(n3)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(user_id)

song_uris = []
year = date.split("-")[0]
for song in song_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False, collaborative=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
