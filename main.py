from dotenv import load_dotenv
import os
import base64
import json
from requests import post, get
import numpy as np
import pandas as pd

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artists with this name exist...")
        return None
    return json_result[0]

def get_artist_id_from_name(token, artist_name):
    result = search_for_artist(token, artist_name)
    artist_id = result["id"] 
    return artist_id

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    if len(json_result) == 0:
        print("This artists doesn't have any tracks...")
        return None
    output = np.repeat([np.array(["Singer", "Song", "ID"], dtype=object)], 10, axis=0)
    for index, song in enumerate(json_result):
        output[index] = [song['artists'][0]['name'], song['name'], song['id']]
    return output
    return json_result

def get_track_features(token, track_id):
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    if len(json_result) == 0:
        print("This artists doesn't have any tracks...")
        return None
    return json_result

token = get_token()
# result = search_for_artist(token, "Michael Jackson")
# artist_id = result["id"]
# SAMPLE_SONG_ID = "5rb9QrpfcKFHM1EUbSIurX"
# songs = get_songs_by_artist(token, artist_id)
# song_ids = np.repeat(SAMPLE_SONG_ID, len(songs))
# print(songs)


# for index, song in enumerate(songs):
#     print(f"{index + 1}. {song['name']} ({song['id']})")
#     song_ids[index] = song['id']

# for id in song_ids[:2]:
#     print(get_track_features(token, id))

# print(get_track_features(token, "63y6xWR4gXz7bnUGOk8iI6"))






