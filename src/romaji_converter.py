import re
import cutlet
from .logger import logger


class RomajiConverter:
    def __init__(self):
        try:
            self.katsu = cutlet.Cutlet()
            self.katsu.use_foreign_spelling = False
            logger.info("MeCab/Cutlet initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize MeCab/Cutlet: {e}")
            logger.warning("Romaji conversion will be disabled")
            self.katsu = None
    
    def is_available(self):
        return self.katsu is not None
    
    def convert_line(self, line):
        if not self.is_available():
            return line
        
        timestamp_pattern = re.compile(r'^(\[\d+:\d+\.\d+\])')
        match = timestamp_pattern.match(line)
        
        if match:
            timestamp = match.group(1)
            lyrics = line[len(timestamp):]
            
            if lyrics.strip():
                try:
                    romaji = self.katsu.romaji(lyrics)
                    # Kapitalisasi huruf pertama
                    romaji = romaji[0].upper() + romaji[1:] if romaji else romaji
                    return f"{timestamp}{romaji}"
                except Exception as e:
                    logger.warning(f"Failed to convert line: {str(e)[:50]}")
                    return line
            else:
                return timestamp
        else:
            return line
    
    def convert_lyrics(self, lyrics_list):
        if not self.is_available():
            logger.warning("Romaji converter not available, returning original lyrics")
            return lyrics_list
        
        converted = []
        for line in lyrics_list:
            converted.append(self.convert_line(line))
        
        return converted