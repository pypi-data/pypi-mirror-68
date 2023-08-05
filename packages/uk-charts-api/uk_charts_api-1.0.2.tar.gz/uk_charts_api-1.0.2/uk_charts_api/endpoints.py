from typing import Union, Dict


class Endpoints:
    @staticmethod
    def track(track_id: str) -> str:
        return f"https://api.deezer.com/track/{track_id}"

    @staticmethod
    def contributor(contributor_id: str) -> str:
        return f"https://api.deezer.com/artist/{contributor_id}"

    @staticmethod
    def album(album_id: str) -> str:
        return f"https://api.deezer.com/album/{album_id}"

    @staticmethod
    def genre(genre_id: str) -> str:
        return f"https://api.deezer.com/genre/{genre_id}"

    @staticmethod
    def search(parameters: Dict[str, Union[str, int]]) -> str:
        end_point = "https://api.deezer.com/search?q="
        for parameter, value in parameters.items():
            end_point += f"{parameter}:'{value}' "
        return end_point

    @staticmethod
    def get_user_data() -> str:
        return "deezer.getUserData"
