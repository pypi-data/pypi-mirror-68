import datetime
from typing import Dict, Generator, List, Optional, Tuple, Union

import bs4
import requests
from bs4 import BeautifulSoup as bs

from .models import chart


class Scraper:
    def __init__(self, date: datetime.date, chart_title: str):
        self.date: datetime.date = date
        self.chart_title: str = chart_title
        self.chart_id = self._chart_id_from_type(self.chart_title)
        self.chart_date = date.strftime("%Y%m%d")
        self.chart_url = self._chart_url(self.chart_title, self.chart_date, self.chart_id)

    def scrape(self) -> Generator[chart.ChartData, None, None]:
        soup: bs = self._download_webpage(self.chart_url)

        rows: List[bs4.element.Tag]
        data_table: bs4.element.Tag
        rows, data_table = self._extract_rows(soup)
        for row in rows:
            if self._is_advertisement(row):
                continue

            chart_song = self._extract_chartsong_metadata(row)
            stream_links = self._extract_stream_links(row, data_table)

            for link in stream_links:
                provider = self._streaming_provider(link)
                if provider == "deezer":
                    deezer_stream_url = link
                elif provider == "spotify":
                    spotify_stream_url = link

            chart_song.set_stream_urls(deezer_stream_url, spotify_stream_url)

            chart_data = self._extract_chartdata_metadata(row, chart_song)
            yield chart_data

    def _chart_id_from_type(self, chart_id: str) -> str:
        chart_ids = {"singles-chart": "7501"}
        return chart_ids[chart_id]

    def _is_advertisement(self, row: bs4.element.Tag) -> bool:

        if row.find(class_="adspace"):
            return True
        else:
            return False

    def _chart_url(self, chart_type: str, chart_date: str, chart_id: str) -> str:
        chart_url = f"http://www.officialcharts.com/charts/{chart_type}/{chart_date}/{chart_id}/"

        return chart_url

    def _download_webpage(self, url: str) -> bs:
        page = requests.get(url)  # DLs the chart page
        soup = bs(page.content, "html.parser")  # Initialises into BS4

        return soup

    def _extract_rows(self, parsed_page: bs) -> Tuple[List[bs4.element.Tag], bs4.element.Tag]:
        data_table = parsed_page.find("table", class_="chart-positions")

        data_rows = data_table.find_all(
            "tr", class_=None
        )  # Creates a list of all the "Rows" of the tablespecial type of row

        return data_rows, data_table

    def _extract_stream_links(self, row: bs4.element.Tag, parsed_page: bs) -> List[str]:
        """ Finds all of the rows with streaming links in.
            Each of these has an index as part of their ID, get this.
        """
        try:
            # Gets all of the links, we only want the first (0th) one
            stream_open_button = row.find_all("div", class_="actions")[0].find_all("a", class_="")[0]

            # Splits the 'data-toggle' id into the hyphenated parts. Only the end part is unique
            stream_open_button_id: int = int(stream_open_button["data-toggle"].split("-")[3])
        except IndexError:
            # The open button doesn't exist in the row,
            # so there are no streaming links
            return []

        stream_elements = parsed_page.find_all("tr", class_=f"actions-view-listen-{stream_open_button_id}")
        stream_links: List[str] = [tag.get("href") for tag in stream_elements[0].find_all("a")]
        # Hopefully, if both Deezer and Spotify stream the song, a list of two links

        return stream_links

    def _streaming_provider(self, link: str) -> Optional[str]:
        if "deezer" in link:
            return "deezer"
        elif "spotify" in link:
            return "spotify"
        else:
            return None

    def _add_stream_links_to_object(self, chart_data: chart.ChartData, deezer: str, spotify: str) -> None:
        chart_data.set_stream_urls(deezer, spotify)

    def _extract_chartsong_metadata(self, row: bs4.element.Tag) -> chart.ChartSong:
        row_data: Dict[str, Union[str, int]] = {}

        row_data["title"] = row.find(class_="title").find("a").get_text()
        row_data["artist"] = row.find(class_="artist").find("a").get_text()
        row_data["label"] = row.find(class_="label").get_text()
        row_data["peak"] = row.find_all("td", recursive=False)[3].get_text()
        row_data["woc"] = row.find_all("td", recursive=False)[4].get_text()
        row_data["position"] = row.find(class_="position").get_text()
        row_data["chart_id"] = self.chart_id

        return chart.ChartSong(row_data)

    def _extract_chartdata_metadata(self, row: bs4.element.Tag, chart_song: chart.ChartSong) -> chart.ChartData:
        # Make some way to have a ChartSong in here in the parameters
        row_data: Dict[str, Union[str, int]] = {}

        row_data["chart_id"] = self.chart_id
        row_data["chart_title"] = self.chart_title
        row_data["chart_song"] = chart_song
        row_data["date"] = self.chart_date
        row_data["chart_url"] = self.chart_url
        row_data["last_week"] = row.find(class_="last-week").get_text().strip()

        # Make sure these corruspond with the ones in ChartData

        return chart.ChartData(row_data)
