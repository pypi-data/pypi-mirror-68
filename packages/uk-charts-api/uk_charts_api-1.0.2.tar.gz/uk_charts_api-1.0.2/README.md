# UK-Charts-API
A repo for the refactor of a set of private scripts that build a sqlite database of the metadata for all Official UK Chart entries

The code here is to be used to scrape the [UK Official Top 40](https://www.officialcharts.com/), then get the metadata from deezer and then downloaded if the user provides a way to do this.

A working example that simply downloads (if downloader provided) all tracks from the UK Charts from its beginning and writes their metadata to a Sqlite database can be found at `example.py`.
