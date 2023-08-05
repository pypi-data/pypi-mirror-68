from typing import Dict, Optional, cast

import requests

from .db import Db
from .endpoints import Endpoints
from .models import deezer
from .sql import Exists, Insert
from .utils import replace_illegals, requests_retry_session


class Deezer:
    # Be careful when debugging this as VSCode's sidebar will call the @property methods
    def __init__(self, arl: str, track_id: str, spotify_url: str = None) -> None:
        self.initialise_counter = 0
        self.initialise(arl, track_id, spotify_url)

    def initialise(self, arl: str, track_id: str, spotify_url: str = None) -> None:
        self.initialise_counter += 1
        self.arl = arl
        self._setup_session()
        self._login_by_arl(self.arl)
        self._get_tokens()
        self.track_id = track_id

        self.lyrics = Lyrics(track_id, self)

        self._raw_track_data: dict = self._request_wrapper(Endpoints.track(track_id))

        self._track_data: deezer.Track = None
        self._album_data: deezer.Album = None
        self._artist_data: deezer.Contributor = None
        self.spotify_url = spotify_url

        self.artist_id = self._raw_track_data["artist"]["id"]
        self.album_id = self._raw_track_data["album"]["id"]

    def _setup_session(self) -> None:
        self.session = requests.Session()
        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/68.0.3440.106 Safari/537.36"
        )
        http_headers = {
            "User-Agent": user_agent,
            "Content-Language": "en-US",
            "Cache-Control": "max-age=0",
            "Accept": "*/*",
            "Accept-Charset": "utf-8,ISO-8859-1;q=0.7,*;q=0.3",
            "Accept-Language": "en-US;q=0.6,en;q=0.4",
            "Connection": "keep-alive",
        }
        self.session.headers.update(http_headers)

    def _login_by_arl(self, arl: str) -> bool:
        cookies = {"arl": arl}
        self.session.cookies.update(cookies)
        req = self._perform_hidden_request(Endpoints.get_user_data())
        if req["USER"]["USER_ID"]:
            return True
        else:
            return False

    def _perform_hidden_request(self, method: str, json_req: dict = {}) -> dict:
        """ Requests info from the hidden api: gw-light.php.
            Used for loginUserToken(), getCSRFToken()
            and privateApi().
        """
        api_token = "null" if method == Endpoints.get_user_data() else self.csrf_token
        unofficial_api_queries = {
            "api_version": "1.0",
            "api_token": api_token,
            "input": "3",
            "method": method,
        }
        req = (
            requests_retry_session(session=self.session)
            .post(url="https://www.deezer.com/ajax/gw-light.php", params=unofficial_api_queries, json=json_req,)
            .json()
        )
        return req["results"]

    def _get_tokens(self) -> None:
        req = self._perform_hidden_request(Endpoints.get_user_data())
        self.csrf_token = req["checkForm"]
        self.sid_token = req["SESSION_ID"]

    def _perform_request(self, end_point: str) -> Optional[Dict]:
        resp = requests_retry_session().get(end_point)
        data = resp.json()

        if "error" in data:
            return None

        return data

    def _request_wrapper(self, end_point: str) -> Optional[Dict]:
        data = self._perform_request(end_point)
        if not data:
            if self.initialise_counter == 3:
                raise ValueError(f"No deezer id for song {self.track_id}")
            search_end_point = Endpoints.search(
                {"track": self._get_track(children=False).title, "artist": self.contributor.name}
            )
            search_data = self._perform_request(search_end_point)
            self.initialise(self.arl, search_data["data"][0]["id"], self.spotify_url)
            data = self._request_wrapper(end_point)

            return data

        return data

    def popular_similar(self) -> "Deezer":
        # Use a string because Deezer isn't defined when Deezer is being defined.
        search_end_point = Endpoints.search({"track": self.track.title, "artist": self.contributor.name})
        data = self._request_wrapper(search_end_point)
        return Deezer(self.arl, data["data"][0]["id"], self.spotify_url)

    def _get_track(self, children: bool = True) -> deezer.Track:
        if self._track_data is None:
            if children:
                self._artist_data = self.contributor
                self._album_data = self.album

                data = self._raw_track_data
                data["artist"] = self._artist_data
                data["album"] = self._album_data
                self._track_data = deezer.Track(data, self.spotify_url, net_req=True)
            else:
                data = self._raw_track_data
                data["artist"] = {}
                data["album"] = {}

                self._track_data = deezer.Track(data, self.spotify_url, net_req=True, skip_children=True)
        return self._track_data

    track: deezer.Track = property(_get_track)

    @property
    def album(self) -> deezer.Album:
        if self._album_data is None:
            raw_album_data = self._request_wrapper(Endpoints.album(self.album_id))
            self._album_data = deezer.Album(raw_album_data, net_req=True)

        return self._album_data

    @property
    def contributor(self) -> deezer.Contributor:
        if self._artist_data is None:
            raw_artist_data = self._request_wrapper(Endpoints.contributor(self.artist_id))
            self._artist_data = deezer.Contributor(raw_artist_data, net_req=True)

        return self._artist_data

    def generate_filepath(self, prefix: str) -> str:
        filepath = f"{prefix}/{self.contributor.name}/{replace_illegals(self.album.title)}/{replace_illegals(self.track.title_short)}"
        return filepath

    def get_lyrics(self, synced: bool = False) -> list:
        if synced:
            return self.lyrics.synced_lyrics()
        else:
            return self.lyrics.unsynced_lyrics()

    def write_record(self, database: Db) -> None:
        self.track.write_record(database)
        self.write_metadata(database)

    def write_metadata(self, database: Db) -> int:
        existing_id = database.exists(Exists.track_metadata, (self.track.isrc,))
        if existing_id:
            db_id = existing_id
        else:
            database.insert(
                Insert.track_metadata,
                (
                    self.track.isrc,
                    self.track_id,
                    self.track.spotify_url,
                    self.track.title,
                    self.track.title_short,
                    self.track.duration,
                    self.track.track_position,
                    self.track.rank,
                    self.track.explicit_lyrics,
                    self.track.bpm,
                    "\n".join(self.lyrics.unsynced_lyrics()),
                ),
            )
            db_id = cast(int, database.cursor.lastrowid)
        return db_id


class Lyrics:
    def __init__(self, track_id: str, deezer: Deezer):
        self.track_id = track_id
        self.deezer = deezer
        self._lyric_data: dict = {}

    def _lyrics_request(self) -> dict:
        self._lyric_data = self.deezer._perform_hidden_request("song.getLyrics", {"sng_id": self.track_id})

        return self._lyric_data

    def unsynced_lyrics(self) -> list:
        if self._lyric_data == {}:
            data = self._lyrics_request()
        else:
            data = self._lyric_data
        if "LYRICS_TEXT" in data:  # unsynced lyrics
            lyrics = data["LYRICS_TEXT"].splitlines()  # True keeps the \n
            return lyrics
        else:
            return []

    def synced_lyrics(self) -> list:
        if self._lyric_data == {}:
            data = self._lyrics_request()
        else:
            data = self._lyric_data
        if "LYRICS_SYNC_JSON" in data:  # synced lyrics
            lyrics = data["LYRICS_SYNC_JSON"]
            return lyrics
        else:
            return []
