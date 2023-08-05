from typing import Any, Dict, Optional

from ..db import Db
from ..deezer import Deezer
from ..sql import Exists, Insert
from ..utils import read_arl, url_to_deezer_id


class ChartSong:
    def __init__(self, data: Dict[str, Any]):
        self.title = data["title"]
        self.artist = data["artist"]
        self.label = data["label"]
        self.woc = data["woc"]  # Unused, can be unreliable from scraper, just calculate from db
        self.peak = data["peak"]
        self.position = data["position"]
        self.chart_id: int = data["chart_id"]
        self.deezer_id: str
        self.spotify_id: str
        self.track: Deezer = None
        self.track_id: Optional[int] = None

    def set_stream_urls(self, deezer_id: str, spotify_id: str) -> None:
        if deezer_id is not None:
            self.deezer_id = deezer_id
        if spotify_id is not None:
            self.spotify_id = spotify_id

    def to_deezer(self) -> Optional[Deezer]:
        try:
            initial_candidate = Deezer(
                read_arl("arl.txt"), url_to_deezer_id(self.deezer_id), spotify_url=self.spotify_id
            )
            if initial_candidate.album.track_count == 1:
                try:
                    song = initial_candidate.popular_similar()
                except ValueError:
                    song = initial_candidate
            else:
                song = initial_candidate

            self.track = song
            self.track_id = song.track_id
            return song
            # if initial_candidate.album.track_list
        except NameError:
            raise ValueError(f"No deezer id for song {self.title} by {self.artist}")

    def get_db_id(self, database: Db) -> int:
        if self.db_id is not None:
            return self.db_id
        else:
            return self.write_record(database)

    def write_record(self, database: Db, chart_db_id: int) -> int:
        self.chart_db_id = chart_db_id
        existing_id = database.exists(Exists.chart_track, (self.chart_db_id, self.track_id))
        if existing_id:
            self.db_id = existing_id
        else:
            database.insert(
                Insert.chart_track, (self.chart_db_id, self.track_id, self.position),
            )
            self.db_id = database.cursor.lastrowid
        return self.db_id


class ChartData:
    def __init__(self, data: Dict[str, Any]):
        self.chart_id = data["chart_id"]
        self.chart_title = data["chart_title"]
        self.chart_song: ChartSong = data["chart_song"]
        self.date = data["date"]
        self.chart_url = data["chart_url"]
        self.last_week = data["last_week"]
        self.db_id: Optional[int] = None

    def get_db_id(self, database: Db) -> int:
        if self.db_id is not None:
            return self.db_id
        else:
            return self.write_record(database)

    def write_record(self, database: Db) -> int:
        existing_id = database.exists(Exists.chart, (self.chart_title, self.chart_url, self.date))
        if existing_id:
            self.db_id = existing_id
        else:
            database.insert(Insert.chart, (self.chart_title, self.chart_url, self.date))
            self.db_id = database.cursor.lastrowid
        self.chart_song.write_record(database, self.get_db_id(database))
        return self.db_id
