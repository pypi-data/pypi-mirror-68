import time
from typing import Any, Optional

import acoustid
from mutagen.id3 import (
    APIC,
    RVA2,
    TALB,
    TBPM,
    TCON,
    TDEN,
    TDRL,
    TIT2,
    TPE1,
    TPE2,
    TPOS,
    TPUB,
    TRCK,
    TRSN,
    TSOA,
    TSOP,
    TSOT,
    TSRC,
    TXXX,
    USLT,
    WXXX,
)
from mutagen.mp3 import MP3

from .deezer import Deezer
from .mb import Musicbrainz
from .utils import sort_title


class Tag:
    def __init__(self, filename: str, deezer: Deezer, ext: str) -> None:
        self.filename = filename
        self.deezer = deezer
        self.ext = ext
        self._tag()

    def add_tag(self, f: MP3, tag: Any) -> None:
        try:
            f.tags.add(tag)
        except ValueError:
            return

    def _calculate_acoustid_fingerprint(self, filename: str) -> list:
        duration, fingerprint = acoustid.fingerprint_file(filename)

        return [duration, fingerprint]

    def _tag_mp3(self, filename: str, deezer: Deezer) -> None:
        f = MP3()

        f.add_tags()

        duration, acoustid_fingerprint = self._calculate_acoustid_fingerprint(filename)
        mb_ids = self._mb_id(deezer.contributor.name, deezer.track.title)

        self.add_tag(f, TPUB(encoding=3, text=deezer.album.label))
        self.add_tag(f, TSOT(encoding=3, text=deezer.track.title))
        self.add_tag(f, TSOA(encoding=3, text=sort_title(deezer.album.title)))
        self.add_tag(f, TSOP(encoding=3, text=deezer.contributor.name))
        self.add_tag(f, TDEN(text=time.strftime("%d/%m/%Y %H:%M:%S")))
        self.add_tag(f, TIT2(encoding=3, text=deezer.track.title))
        self.add_tag(f, TPOS(text=str(deezer.track.disk_number)))
        self.add_tag(f, TRCK(text=str(deezer.track.track_position)))
        self.add_tag(f, TDRL(text=deezer.album.id3v24_release_date))
        self.add_tag(f, TPE1(text=deezer.album.contributors))
        self.add_tag(f, TPE2(text=deezer.contributor.name))
        self.add_tag(f, TBPM(text=str(deezer.track.bpm)))
        self.add_tag(f, RVA2(desc="", channel=1, gain=deezer.track.gain))
        self.add_tag(f, USLT(text=deezer.lyrics.unsynced_lyrics()))
        self.add_tag(f, TCON(text=deezer.album.genre_list))
        self.add_tag(f, TXXX(text=deezer.album.upc, desc="upc"))
        self.add_tag(f, TALB(text=deezer.album.title))
        self.add_tag(f, WXXX(url=deezer.album.link, desc="album_deezer_url"))
        self.add_tag(f, WXXX(url=deezer.track.link, desc="song_deezer_url"))
        self.add_tag(f, WXXX(url=deezer.contributor.link, desc="artist_deezer_url"))
        self.add_tag(f, WXXX(url=deezer.track.spotify_url, desc="song_spotify_id"))
        self.add_tag(f, WXXX(url=acoustid_fingerprint, desc="acoust_id_fingerprint"))
        self.add_tag(
            f, APIC(type=3, data=deezer.album.cover.cover_art(1500), mime="image/jpeg")
        )  # 8 is artist, 3 is album
        self.add_tag(
            f, APIC(type=3, data=deezer.contributor.picture.cover_art(1500), mime="image/jpeg")
        )  # 8 is artist, 3 is album
        self.add_tag(f, TSRC(text=deezer.track.isrc))
        self.add_tag(f, TRSN(text="Deezer"))

        if mb_ids is not None:
            self.add_tag(f, TXXX(text=mb_ids["artist"], desc="musicbrainz_albumartistid"))
            self.add_tag(f, TXXX(text=mb_ids["album"], desc="musicbrainz_albumid"))
            self.add_tag(f, TXXX(text=mb_ids["quality"], desc="musicbrainz_id_quality"))

        f.save(filename)

    def _mb_id(self, artist: str, title: str) -> Optional[dict]:
        mb = Musicbrainz(artist, title)
        primary = mb.primary_mb_release

        if primary is None:
            return None

        try:
            ar_id = primary["artist-credit"][0]["artist"]["id"]
            al_id = primary["id"]
            qual = primary["mb_type"]
        except KeyError:  # There is somehow no artist or album id(?)
            return None

        data = {"artist": ar_id, "album": al_id, "quality": qual}
        return data

    def _tag(self) -> None:
        """ Function to write tags to the file, be it FLAC or MP3."""
        # retrieve tags

        if self.ext == ".mp3":
            self._tag_mp3(self.filename, self.deezer)
        else:
            raise NotImplementedError("Could not write tags. File extension not supported.")
