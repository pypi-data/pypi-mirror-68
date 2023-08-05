import datetime
from typing import Any, Dict, List, Optional, cast

from ..db import Db
from ..endpoints import Endpoints
from ..sql import Exists, Insert
from ..utils import dict_rename, requests_retry_session


class Track:
    def __init__(
        self, data: Dict[str, Any], spotify_url: str = None, net_req: bool = False, skip_children: bool = False
    ):
        if net_req:
            data = self._net_req_convert(data, skip_children)

        self.deezer_id: str = data["deezer_id"]
        self.title: str = data["title"]
        self.title_short: str = data["title_short"]
        self.isrc: str = data["isrc"]
        self.link: str = data["link"]
        self.duration: int = data["duration"]
        self.track_position: int = data["track_position"]
        self.disk_number: int = data["disk_number"]
        self.rank: int = data["rank"]
        self.release_date: datetime.date = data["release_date"]
        self.explicit_lyrics: bool = data["explicit_lyrics"]
        self.preview_url: str = data["preview_url"]
        self.bpm: int = data["bpm"]
        self.gain: float = data["gain"]
        self.contributors: List[int] = data["contributors"]
        self.artist: Contributor = data["artist"]
        self.album: Album = data["album"]
        self.spotify_url: Optional[str] = spotify_url

        if "title_version" in data:
            self.title_version: str = data["title_version"]

        self.db_id: Optional[int] = None

    def _net_req_convert(self, data: Dict[str, Any], skip_children: bool = False) -> Dict[str, Any]:
        rename = {"id": "deezer_id", "preview": "preview_url"}
        remove = [
            "share",
            "explicit_content_lyrics",
            "explicit_content_cover",
            "available_countries",
        ]

        for original, new in rename.items():
            data[new] = data[original]
            data.pop(original)

        for field in remove:
            data.pop(field)

        data["contributors"] = [contrib_data["id"] for contrib_data in data["contributors"]]

        if not skip_children:
            if not isinstance(data["artist"], Contributor):
                data["artist"] = Contributor(data["artist"])
            if not isinstance(data["album"], Album):
                data["album"] = Album(data["album"])

        return data

    def get_db_id(self, database: Db) -> int:
        if self.db_id is not None:
            return self.db_id
        else:
            return self.write_record(database)

    def write_record(self, database: Db) -> int:
        existing_id = database.exists(Exists.track, (self.isrc,))
        if existing_id:
            self.db_id = existing_id
        else:
            database.insert(
                Insert.track, (self.isrc, self.artist.get_db_id(database), self.album.get_db_id(database), None)
            )
            self.db_id = cast(int, database.cursor.lastrowid)
        return self.db_id


class Contributor:
    def __init__(self, data: Dict[str, Any], net_req: bool = False):
        if net_req:
            data = self._net_req_convert(data)
        self.id: int = data["id"]
        self.name: str = data["name"]
        self.link: str = data["link"]
        self.picture: Picture = data["picture"]
        self.albums: int = data["albums"]
        self.fans: int = data["fans"]
        self.track_list: str = data["track_list"]

        self.db_id: Optional[int] = None

    def _net_req_convert(self, data: Dict[str, Any]) -> Dict[str, Any]:
        removed = ["share", "radio", "type"]
        renamed = {"nb_album": "albums", "nb_fan": "fans", "tracklist": "track_list"}

        for field in removed:
            data.pop(field)

        for original, new in renamed.items():
            data[new] = data[original]
            data.pop(original)

        data["picture"] = Picture(data, net_req=True)

        return data

    def get_db_id(self, database: Db) -> int:
        if self.db_id is not None:
            return self.db_id
        else:
            return self.write_record(database)

    def write_record(self, database: Db) -> int:
        existing_id = database.exists(Exists.contributor, (self.id, None, self.name))
        if existing_id:
            self.db_id = existing_id
        else:
            database.insert(Insert.contributor, (self.id, None, self.name, self.fans, self.picture.get_db_id(database)))
            self.db_id = cast(int, database.cursor.lastrowid)
        return self.db_id


class Picture:
    def __init__(self, data: Dict[str, Any], net_req: bool = False, prefix: str = "picture"):
        if net_req:
            data = self._net_req_convert(data, prefix)

        self.thumbnail: dict = {}
        self.small: dict = {}
        self.medium: dict = {}
        self.big: dict = {}
        self.xl: dict = {}

        self.thumbnail["size"] = [120, 120]

        self.thumbnail["url"] = data["thumbnail"]

        if all(size in data.keys() for size in ["small", "medium", "big", "xl"]):
            self.small["size"] = [56, 56]
            self.small["url"] = data["small"]

            self.medium["url"] = data["medium"]
            self.medium["size"] = [250, 250]

            self.big["url"] = data["big"]
            self.big["size"] = [500, 500]

            self.xl["url"] = data["xl"]
            self.xl["size"] = [1000, 1000]

        self.db_id: Optional[int] = None

    def _net_req_convert(self, data: Dict[str, Any], prefix: str = "picture") -> Dict[str, Any]:
        keys = {
            f"{prefix}": "thumbnail",
            f"{prefix}_small": "small",
            f"{prefix}_medium": "medium",
            f"{prefix}_big": "big",
            f"{prefix}_xl": "xl",
        }

        picture_data = {}

        try:
            for original, new in keys.items():
                picture_data[new] = data[original]
        except KeyError:  # Only a single image
            return picture_data
        return picture_data

    @property
    def _url_prefix(self) -> str:
        return "/".join(self.xl["url"].split("/")[0:-1])

    def cover_art(self, size: int) -> bytes:
        """ Retrieves the cover art/playlist image from the official API,
            downloads and returns it.
        """
        url = f"{self._url_prefix}/{size}x{size}.png"
        r = requests_retry_session().get(url)
        return r.content

    def get_db_id(self, database: Db) -> int:
        if self.db_id is not None:
            return self.db_id
        else:
            return self.write_record(database)

    def _write_image_file_record(self, database: Db, image: dict) -> int:
        existing_id = database.exists(Exists.image_file, (image["url"],))
        if existing_id:
            return existing_id
        else:
            database.insert(Insert.image_file, (image["url"], image["size"][0], image["size"][1], True))
            return database.cursor.lastrowid

    def write_image_file(self, database: Db) -> None:
        if all([self.xl == {}, self.big == {}, self.medium == {}, self.small == {}]):
            images = [self.thumbnail]
        else:
            images = [self.thumbnail, self.small, self.medium, self.big, self.xl]
        for i, image in enumerate(images):
            images[i]["db_id"] = self._write_image_file_record(database, image)

    def write_record(self, database: Db) -> int:
        if all([self.xl == {}, self.big == {}, self.medium == {}, self.small == {}]):
            image_ids = (self._write_image_file_record(database, self.thumbnail), None, None, None, None)
            existing_id = database.exists(Exists.photo, image_ids)
        else:
            images = [self.thumbnail, self.small, self.medium, self.big, self.xl]
            image_ids = tuple(self._write_image_file_record(database, image) for image in images)
            existing_id = database.exists(Exists.photo, image_ids)
        if existing_id:
            self.db_id = existing_id
        else:
            self.write_image_file(database)
            database.insert(Insert.photo, image_ids)
            self.db_id = cast(int, database.cursor.lastrowid)
        return self.db_id


class Album:
    def __init__(self, data: Dict[str, Any], net_req: bool = False):
        if net_req:
            data = self._net_req_convert(data)

        self.id: int = data["id"]
        self.title: str = data["title"]
        self.upc: str = data["upc"]
        self.link: str = data["link"]
        self.cover: Picture = data["cover"]
        self.genres: List[Genre] = data["genres"]
        self.label: str = data["label"]
        self.duration: int = data["duration"]
        self.fans: int = data["fans"]
        self.rating: int = data["rating"]
        self.release_date: datetime.date = data["release_date"]
        self.record_type = data["record_type"]
        self.track_list: str = data["track_list"]
        self.explicit_lyrics: bool = data["explicit_lyrics"]
        self.explicit_content_lyrics: bool = data["explicit_content_lyrics"]
        self.explicit_content_cover: bool = data["explicit_content_cover"]
        self.contributors: List[int] = data["contributors"]
        self.artist: Contributor = data["artist"]
        self.track_count: int = data["track_count"]

        self.db_id: Optional[int] = None

    @property
    def id3v24_release_date(self) -> str:
        return self.release_date.strftime("%Y%m%d")

    @property
    def genre_list(self) -> List[str]:
        genres = [genre.name for genre in self.genres]
        return genres

    def _net_req_convert(self, data: Dict[str, Any]) -> Dict[str, Any]:

        rename = {"tracklist": "track_list", "nb_tracks": "track_count"}
        cover_keys = ["cover", "cover_small", "cover_medium", "cover_big", "cover_xl"]

        data["contributors"] = [contrib_data["id"] for contrib_data in data["contributors"]]
        data["genres"] = [Genre(genre_data, net_req=True) for genre_data in data["genres"]["data"]]
        data["release_date"] = datetime.datetime.strptime(data["release_date"], "%Y-%m-%d")

        # Note, this always runs, even when there already is complete data.
        artist_data = self._perform_request(Endpoints.contributor(data["artist"]["id"]))

        data["artist"] = Contributor(artist_data, net_req=True)

        cover_data = {}
        for key in cover_keys:
            cover_data[key] = data[key]

        data["cover"] = Picture(cover_data, net_req=True, prefix="cover")

        data = dict_rename(data, rename)

        # Means that a Track() doesn't reference an Album() that contains the same Track()
        data.pop("tracks")

        return data

    def _perform_request(self, end_point: str) -> Optional[Dict]:
        resp = requests_retry_session().get(end_point)
        data = resp.json()

        if "error" in data:
            return None

        return data

    def get_db_id(self, database: Db) -> int:
        if self.db_id is not None:
            return self.db_id
        else:
            return self.write_record(database)

    def write_record(self, database: Db) -> int:
        existing_id = database.exists(Exists.album, (self.id, None, self.title, self.artist.get_db_id(database)))
        if existing_id:
            self.db_id = existing_id
        else:
            genre_db_ids = [genre.get_db_id(database) for genre in self.genres]
            database.insert(
                Insert.album,
                (
                    self.id,
                    None,
                    self.title,
                    self.artist.get_db_id(database),
                    str(self.contributors),
                    str(genre_db_ids),
                    self.duration,
                    self.release_date,
                    self.cover.get_db_id(database),
                ),
            )
            self.db_id = cast(int, database.cursor.lastrowid)
        return self.db_id


class Genre:
    def __init__(self, data: Dict[str, Any], net_req: bool = False):
        if net_req:
            data = self._net_req_convert(data)

        self.id: int = data["id"]
        self.name: str = data["name"]
        self.picture: Picture = data["picture"]

        self.db_id: Optional[int] = None

    def _net_req_convert(self, data: dict) -> dict:
        genre_data = self._perform_request(Endpoints.genre(str(data["id"])))
        genre_data = cast(dict, genre_data)

        data["picture"] = Picture(genre_data, net_req=True, prefix="picture")

        return data

    def _perform_request(self, end_point: str) -> Optional[Dict]:
        resp = requests_retry_session().get(end_point)
        data = resp.json()

        if "error" in data:
            return None

        return data

    def get_db_id(self, database: Db) -> int:
        if self.db_id is not None:
            return self.db_id
        else:
            return self.write_record(database)

    def write_record(self, database: Db) -> int:
        existing_id = database.exists(Exists.genre, (self.name,))
        if existing_id:
            self.db_id = existing_id
        else:
            database.insert(Insert.genre, (self.name, self.picture.get_db_id(database)))
            self.db_id = cast(int, database.cursor.lastrowid)
        return self.db_id
