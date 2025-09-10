from .lyrics import getLyrics


def _parse_tracks(tracks, syncpoints):
    trackList = []

    for track in tracks:
        __info = {}
        __info["id"] = track.get("id")
        attr = track["attributes"]

        __file = "{0}. {1}".format(
            str(attr.get("trackNumber", 1)).zfill(2),
            attr.get("name", "Unknown Track")
        )
        __info["file"] = __file

        if "lyrics" in track["relationships"]:
            lyrics_data = track["relationships"]["lyrics"].get("data")
            if lyrics_data and len(lyrics_data) > 0:
                ttml = lyrics_data[0]["attributes"].get("ttml")
                __info["ttml"] = ttml
                __info.update(getLyrics(ttml, syncpoints))

        trackList.append(__info)

    return trackList


def album(data, syncpoints):
    tracks = data["data"][0]["relationships"]["tracks"]["data"]
    return _parse_tracks(tracks, syncpoints)


def song(data, syncpoints):
    tracks = data["data"]
    return _parse_tracks(tracks, syncpoints)
