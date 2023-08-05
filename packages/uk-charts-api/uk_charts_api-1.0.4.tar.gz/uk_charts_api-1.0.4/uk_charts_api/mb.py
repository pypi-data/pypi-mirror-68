from typing import Optional

import musicbrainzngs


class Musicbrainz:
    """ Class is used to make sure the release of the ID supplied as
        query_string is the main one.
    """

    def __init__(self, artist: str, title: str) -> None:
        musicbrainzngs.set_useragent("UK Chart Scraper", 1.0)

        self.artist = artist
        self.title = title
        self.mb_releases = self.search(self.artist, self.title)

        if self.mb_releases is None:
            self.primary_mb_release = None
        else:
            self.primary_mb_release = self.mb_releases[0]

    def search(self, artist: str, title: str) -> Optional[list]:
        possible_recordings = musicbrainzngs.search_recordings(
            query=f'title:"{title}" AND artistname:"{artist}" AND primarytype:"Album" AND status:"Official"', limit=100
        )["recording-list"]

        if len(possible_recordings) == 0:
            return None

        pristine_releases: list = []
        emergency_releases: list = []
        dire_releases: list = []

        for recording in possible_recordings:  # A recording is the sound made
            for release in recording["release-list"]:  # A release is the disc the sound is on
                release_type = self._classify_release(release)
                release["mb_type"] = release_type
                if release_type == "pristine":
                    if len(pristine_releases) == 0:
                        pristine_releases.append(release)
                    else:
                        pristine_releases = self._sort_countries(pristine_releases, release)
                elif release_type == "emergency":
                    # Just in case there are no perfect candidates
                    emergency_releases.append(release)
                elif release_type == "dire":
                    # Really bad releases that we really don't want
                    dire_releases.append(release)

        return self._prioritise_releases(pristine_releases, emergency_releases, dire_releases)

    def _prioritise_releases(self, pristine: list, emergency: list, dire: list) -> list:
        releases = []
        if len(pristine) == 0:
            if len(emergency) == 0:
                releases = dire
            else:
                releases = emergency
                releases.sort(key=lambda release: release["date"])
        else:
            releases = pristine

        return releases

    def _classify_release(self, release: dict) -> str:
        if (
            "secondary-type-list" not in release["release-group"]
            and "artist-credit-phrase" in release
            and release["artist-credit-phrase"] != "Various Artists"
            and "date" in release
        ):
            # Having a secondary-type-list means it's a compilation or something else unwanted
            return "pristine"
        elif "artist-credit-phrase" not in release and "date" in release:
            # Just in case there are no perfect candidates
            return "emergency"
        else:
            # Really bad releases that we really don't want
            return "dire"

    def _sort_countries(self, final_releases: list, release: dict) -> list:
        """ Inserts the release into the final_releases list favouring
            British releases, then European, then everywhere else.
        """

        if "country" not in release and "date" not in release:
            # Results like these do not have enough data to
            # be the best result.
            return final_releases
        if release["country"] == "GB":
            # Prefer UK releases
            release_list_index = 0
            while release["date"] > final_releases[release_list_index]["date"]:
                # Oldest UK releases first
                release_list_index += 1
                if release_list_index == len(final_releases):
                    break
            final_releases.insert(release_list_index, release)
        elif release["country"] == "XE":
            release_list_index = 0
            while final_releases[release_list_index]["country"] == "GB":
                # Keep going until all UK releases have been passed
                release_list_index += 1
            final_releases.insert(release_list_index, release)
        else:
            final_releases.append(release)

        return final_releases
