import json
import requests
from secrets import spotify_user_id, new_id
from datetime import date
from refresh import Refresh


class SaveSongs:
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = ""
        self.new_id = new_id
        self.tracks = ""
        self.new_play_list_id = ""

    def find_songs(self):

        print("Finding songs in new realeases...")
        # loop through tracks, add to a list
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(new_id)

        response = requests.get(query,
                                headers={"Content-Type": "appplication/json",
                                         "Authorization": "Bearer {}".format(self.spotify_token)})

        response_json = response.json()
        print(response)

        for i in response_json["items"]:
            self.tracks += (i["track"]["uri"] + ",")
        self.tracks = self.tracks[:-1]

        self.add_to_playlist()

    def create_playlist(self):
        # create the new playlist
        print("creating playlist...")
        today = date.today()

        todayFormatted = today.strftime("%d/%m/%Y")

        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            spotify_user_id)

        request_body = json.dumps({
            "name": todayFormatted + " new releases", "description": "NEW SONGS", "public": False
        })

        response = requests.post(query, data=request_body, headers={"Content-Type": "appplication/json",
                                                                    "Authorization": "Bearer {}".format(self.spotify_token)
                                                                    })

        response_json = response.json()

        return response_json["id"]

    def add_to_playlist(self):
        # add all songs to new playlist

        print("adding songs to your playlist...")

        self.new_play_list_id = self.create_playlist()

        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(
            self.new_play_list_id, self.tracks)

        response = requests.post(query, headers={"Content-Type": "appplication/json",
                                                 "Authorization": "Bearer {}".format(self.spotify_token)
                                                 })

        print(response.json)

    def call_refresh(self):

        print("refreshing token...")

        refreshCaller = Refresh()

        self.spotify_token = refreshCaller.refresh()

        self.find_songs()


a = SaveSongs()
a.call_refresh()
