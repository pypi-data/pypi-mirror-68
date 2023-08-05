class Insert:
    """Insert statements for all tables will eventually be included here
    """

    chart = """INSERT INTO "chart" (
            chart_id,
            name,
            url,
            date)
        VALUES (null, ?, ?, ?)
    """

    image_file = """INSERT INTO "image_file" (
            image_file_id,
            filepath,
            width,
            height,
            url)
        VALUES (null, ?, ?, ?, ?)
    """

    audio_file = """INSERT INTO "audio_file" (
            audio_file_id,
            filepath,
            format,
            bitrate,
            sample_rate,
            bits,
            channels,
            download_time)
        VALUES (null, ?, ?, ?, ?, ?, ?, ?)
    """

    photo = """INSERT INTO "photo" (
            photo_id,
            thumbnail_id,
            small_id,
            medium_id,
            big_id,
            xl_id)
        VALUES (null, ?, ?, ?, ?, ?)
    """

    chart_track = """INSERT INTO "chart_track" (
            chart_track_id,
            chart_id,
            track_id,
            position)
        VALUES (null, ?, ?, ?)
    """

    contributor = """INSERT INTO "contributor" (
            contributor_id,
            deezer_id,
            spotify_id,
            name,
            deezer_fans,
            photo_id)
        VALUES (null, ?, ?, ?, ?, ?)
    """

    album = """INSERT INTO "album" (
            album_id,
            deezer_id,
            spotify_id,
            title,
            primary_contributor,
            contributors,
            genre,
            duration,
            release_date,
            cover)
        VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    genre = """INSERT INTO "genre" (
            genre_id,
            name,
            photo)
        VALUES (null, ?, ?)
    """

    track = """INSERT INTO "track" (
            track_id,
            isrc,
            contributor_id,
            album_id,
            audio_file_id)
        VALUES (null, ?, ?, ?, ?)
    """

    track_metadata = """INSERT INTO "track_metadata" (
            isrc,
            deezer_id,
            spotify_id,
            title,
            short_title,
            duration,
            track_number,
            deezer_rank,
            explicit,
            bpm,
            lyrics)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """


class Update:
    """ Any update queries that can be performed on the database
    """

    set_track_audio_file = """
        UPDATE track
        SET audio_file_id = ?
        WHERE track_id = ?
    """


class Select:
    """Any needed select statements will be here
    """

    pass


class Exists:
    chart = """
        SELECT *
        FROM chart
        WHERE
            name = ? and
            url = ? and
            date = ?
    """

    image_file = """
        SELECT *
        FROM image_file
        WHERE filepath = ?
    """

    audio_file = """
        SELECT *
        FROM  audio_file
        WHERE filepath = ?
    """

    photo = """
        SELECT *
        FROM photo
        WHERE
            thumbnail_id = ? or
            small_id = ? or
            medium_id = ? or
            big_id = ? or
            xl_id = ?
    """

    chart_track = """
        SELECT *
        FROM chart_track
        WHERE
            chart_id = ? and
            track_id = ?
    """

    contributor = """
        SELECT *
        FROM contributor
        WHERE
            (deezer_id = ? or spotify_id = ?) and
            name = ?
    """

    album = """
        SELECT *
        FROM album
        WHERE
            (deezer_id = ? or spotify_id = ?) and
            title = ? and
            primary_contributor = ?
    """

    genre = """
        SELECT *
        FROM genre
        WHERE name = ?
    """

    track = """
        SELECT *
        FROM track
        WHERE isrc = ?
    """

    track_metadata = """
        SELECT *
        FROM track_metadata
        WHERE isrc = ?
    """


class Create:
    chart = """CREATE TABLE IF NOT EXISTS "chart" (
        "chart_id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        "name"    TEXT NOT NULL,
        "url"    TEXT NOT NULL,
        "date"    TIMESTAMP NOT NULL
    )"""

    image_file = """CREATE TABLE IF NOT EXISTS "image_file" (
        "image_file_id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        "filepath"    TEXT NOT NULL UNIQUE,
        "width"    INTEGER NOT NULL,
        "height"    INTEGER NOT NULL,
        "url"    INTEGER NOT NULL
    )"""

    audio_file = """CREATE TABLE IF NOT EXISTS "audio_file" (
        "audio_file_id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        "filepath"    TEXT NOT NULL UNIQUE,
        "format"    TEXT NOT NULL CHECK(format="mp3" or "flac"),
        "bitrate"    INTEGER NOT NULL,
        "sample_rate"    INTEGER NOT NULL,
        "bits"    INTEGER NOT NULL,
        "channels"    INTEGER NOT NULL,
        "download_time"    TIMESTAMP NOT NULL
    )"""

    photo = """CREATE TABLE IF NOT EXISTS "photo" (
        "photo_id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        "thumbnail_id"    INTEGER,
        "small_id"    INTEGER,
        "medium_id"    INTEGER,
        "big_id"    INTEGER,
        "xl_id"    INTEGER,
        FOREIGN KEY("xl_id") REFERENCES "image_file"("image_file_id"),
        FOREIGN KEY("big_id") REFERENCES "image_file"("image_file_id"),
        FOREIGN KEY("medium_id") REFERENCES "image_file"("image_file_id"),
        FOREIGN KEY("small_id") REFERENCES "image_file"("image_file_id"),
        FOREIGN KEY("thumbnail_id") REFERENCES "image_file"("image_file_id")
    )"""

    chart_track = """CREATE TABLE IF NOT EXISTS "chart_track" (
        "chart_track_id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        "chart_id"    INTEGER NOT NULL,
        "track_id"    INTEGER,
        "position"    INTEGER,
        FOREIGN KEY("chart_id") REFERENCES "chart"("chart_id"),
        FOREIGN KEY("track_id") REFERENCES "track"("track_id")
    )"""

    contributor = """CREATE TABLE IF NOT EXISTS "contributor" (
        "contributor_id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        "deezer_id"    INTEGER UNIQUE,
        "spotify_id"    TEXT UNIQUE,
        "name"    TEXT,
        "deezer_fans"    INTEGER,
        "photo_id"    INTEGER,
        FOREIGN KEY("photo_id") REFERENCES "photo"("photo_id")
    )"""

    album = """CREATE TABLE IF NOT EXISTS "album" (
        "album_id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        "deezer_id"    INTEGER UNIQUE,
        "spotify_id"    TEXT UNIQUE,
        "title"    TEXT,
        "primary_contributor"    INTEGER,
        "contributors"    TEXT,
        "genre"    INTEGER,
        "duration"    INTEGER,
        "release_date"    TIMESTAMP,
        "cover"    INTEGER,
        FOREIGN KEY("cover") REFERENCES "photo"("photo_id"),
        FOREIGN KEY("primary_contributor") REFERENCES "contributor"("contributor_id")
    )"""

    genre = """CREATE TABLE IF NOT EXISTS "genre" (
        "genre_id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        "name"    TEXT UNIQUE,
        "photo"    INTEGER,
        FOREIGN KEY("photo") REFERENCES "genre"("genre_id")
    )"""

    track = """CREATE TABLE IF NOT EXISTS "track" (
        "track_id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        "isrc"    TEXT NOT NULL UNIQUE,
        "contributor_id"    INTEGER NOT NULL,
        "album_id"    INTEGER NOT NULL,
        "audio_file_id"    INTEGER,
        FOREIGN KEY("contributor_id") REFERENCES "contributor"("contributor_id"),
        FOREIGN KEY("album_id") REFERENCES "album"("album_id"),
        FOREIGN KEY("isrc") REFERENCES "track_metadata"("isrc")
    )"""

    track_metadata = """CREATE TABLE IF NOT EXISTS "track_metadata" (
        "isrc"    TEXT NOT NULL UNIQUE,
        "deezer_id"    INTEGER,
        "spotify_id"    INTEGER,
        "title"    TEXT,
        "short_title"    TEXT,
        "duration"    INTEGER,
        "track_number"    INTEGER,
        "deezer_rank"    INTEGER,
        "explicit"    INTEGER NOT NULL CHECK(explicit = 1 or explicit = 0),
        "bpm"    REAL,
        "lyrics"    TEXT,
        PRIMARY KEY("isrc")
    )"""
