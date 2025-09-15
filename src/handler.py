import os
from sanitize_filename import sanitize
from .api import AppleMusic
from .logger import logger


def __get_path():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def handler(args):
    syncpoints = 3 if args.sync else 2

    downloaded_files = []
    skipped_files = []

    for url in args.urls:
        logger.info(f"Processing URL: {url}")
        apple_music = AppleMusic(
            cache=os.path.join(__get_path(), "cache"),
            config=os.path.join(__get_path(), "config"),
            sync=syncpoints
        )
        data_from_api = apple_music.getInfo(url)

        lyrics_folder = os.path.join(__get_path(), "downloads")
        os.makedirs(lyrics_folder, exist_ok=True)

        track_list = (
            data_from_api["tracks"]
            if isinstance(data_from_api, dict) and "tracks" in data_from_api
            else data_from_api
        )

        for track in track_list:
            file_name = sanitize(track.get("file"))
            path = os.path.join(lyrics_folder, f"{file_name}.lrc")

            if os.path.exists(path):
                logger.warning(f'"{file_name}.lrc" already exists!')
                skipped_files.append(file_name)
                continue

            if track.get("timeSyncedLyrics"):
                logger.info(f'Saving "{file_name}.lrc"...')
                with open(path, "w", encoding="utf-8") as f:
                    f.write("\n".join(track["timeSyncedLyrics"]))
                downloaded_files.append(file_name)
            else:
                logger.warning(f'No time-synced lyrics for "{file_name}"')
                skipped_files.append(file_name)

    logger.done(f"{len(downloaded_files)} file(s) downloaded, {len(skipped_files)} file(s) skipped.")
