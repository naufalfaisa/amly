import os
from sanitize_filename import sanitize
from .api import AppleMusic
from .logger import logger
from .romaji_converter import RomajiConverter


def __get_path():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def handler(args):
    """
    Main handler logic for processing Apple Music URLs.
    Downloads lyrics (synced or unsynced) and optionally converts to Romaji.
    """
    syncpoints = 3 if args.sync else 2
    downloaded_files = []
    skipped_files = []

    romaji_converter = None
    if args.romaji:
        romaji_converter = RomajiConverter()
        if not romaji_converter.is_available():
            logger.warning("Romaji conversion requested but MeCab is not available")

    for url in args.urls:
        logger.info(f"Processing URL: {url}")

        # Initialize AppleMusic API client
        apple_music = AppleMusic(
            cache=os.path.join(__get_path(), "cache"),
            config=os.path.join(__get_path(), "config"),
            sync=syncpoints
        )
        data_from_api = apple_music.getInfo(url)

        lyrics_folder = os.path.join(__get_path(), "downloads")
        os.makedirs(lyrics_folder, exist_ok=True)

        # Handle both album (list of tracks) and single song (dict) responses
        track_list = (
            data_from_api["tracks"]
            if isinstance(data_from_api, dict) and "tracks" in data_from_api
            else data_from_api
        )

        for track in track_list:
            file_name = sanitize(track.get("file"))
            suffix = "_romaji" if (args.romaji and romaji_converter and romaji_converter.is_available()) else ""
            path = os.path.join(lyrics_folder, f"{file_name}{suffix}.lrc")

            if os.path.exists(path):
                logger.warning(f'"{file_name}{suffix}.lrc" already exists!')
                skipped_files.append(file_name)
                continue

            # Time-synced lyrics
            if track.get("timeSyncedLyrics"):
                logger.info(f'Saving time-synced lyrics "{file_name}{suffix}.lrc"...')

                lyrics_to_save = track["timeSyncedLyrics"]

                if args.romaji and romaji_converter and romaji_converter.is_available():
                    logger.info('Converting to romaji...')
                    lyrics_to_save = romaji_converter.convert_lyrics(lyrics_to_save)

                with open(path, "w", encoding="utf-8") as f:
                    f.write("\n".join(lyrics_to_save))

                downloaded_files.append(file_name)
                continue

            # Unsynced lyrics fallback
            logger.warning(f'No time-synced lyrics for "{file_name}". Using unsynced lyrics.')

            unsynced = (
                track.get("lyrics")
                or track.get("unSyncedLyrics")
                or track.get("plainLyrics")
                or None
            )

            if not unsynced:
                logger.error(f'No lyrics available for "{file_name}".')
                skipped_files.append(file_name)
                continue

            if args.romaji and romaji_converter and romaji_converter.is_available():
                logger.info('Converting to romaji...')
                unsynced = romaji_converter.convert_lyrics(unsynced)

            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(unsynced))

            downloaded_files.append(file_name)

    logger.done(f"{len(downloaded_files)} file(s) downloaded, {len(skipped_files)} file(s) skipped.")
