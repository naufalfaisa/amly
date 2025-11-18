import re
import json
import requests

from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

from .cache import Cache
from .logger import logger
from .config import Configure
from .tracks import album, song

HEADERS = {
    'content-type': 'application/json;charset=utf-8',
    'connection': 'keep-alive',
    'accept': 'application/json',
    'origin': 'https://music.apple.com',
    'referer': 'https://music.apple.com/',
    'accept-encoding': 'gzip, deflate, br',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}


class AppleMusic(object):
    def __init__(self, cache: str, config: str, sync: int):
        self.__session = requests.Session()
        self.__session.headers = HEADERS

        self.__cache = Cache(cache)
        self.__config = Configure(config)

        self.sync = sync

        self.__accessToken()
        self.__mediaUserToken()

    def __checkUrl(self, url):
        try:
            urlopen(url)
            return True
        except (URLError, HTTPError):
            return False

    def __getUrl(self, url):
        __url = urlparse(url)

        if not __url.scheme:
            url = f"https://{url}"

        if __url.netloc == "music.apple.com":
            if self.__checkUrl(url):
                splits = url.split('/')

                id = splits[-1]
                kind = splits[4]

                if kind == "album":
                    if len(id.split('?i=')) > 1:
                        id = id.split('?i=')[1]
                        kind = "song"

                self.kind = kind
                self.id = id

            else: logger.error("URL is invalid!", 1)
        else: logger.error("URL is invalid!", 1)

    def __accessToken(self):
        while True:
            accessToken = self.__cache.get("accessToken")

            if not accessToken:
                logger.info("Access token not found in cache. Fetching from web...")
                try:
                    response = requests.get('https://music.apple.com/us/browse', timeout=10)
                    response.raise_for_status()
                    indexJs = re.search(r'(?<=index)(.*?)(?=\.js")', response.text).group(1)

                    response_js = requests.get(f'https://music.apple.com/assets/index{indexJs}.js', timeout=10)
                    response_js.raise_for_status()

                    accessToken = re.search(r'(?=eyJh)(.*?)(?=")', response_js.text).group(1)
                    if not accessToken:
                        raise ValueError("Access token not found in JS file.")

                    self.__cache.set("accessToken", accessToken)
                    logger.info("Access token fetched successfully.")
                    
                except Exception as e:
                    logger.warning(f"Failed to fetch token automatically: {e}")
                    accessToken = input("Enter your media-user-token manually: ").strip()
                    if not accessToken:
                        logger.error("No token entered. Cannot continue.", 1)
                        return
                    self.__cache.set("accessToken", accessToken)

            self.__session.headers.update({'authorization': f'Bearer {accessToken}'})

            try:
                test_response = self.__session.get(
                    "https://amp-api.music.apple.com/v1/catalog/us/songs/1450330685",
                    timeout=10
                )
                if test_response.status_code == 200 and test_response.text:
                    logger.info("Access token is valid.")
                    break
                else:
                    logger.info("Access token expired or invalid. Removing from cache...")
                    self.__cache.delete("accessToken")
                    
            except requests.RequestException as e:
                logger.warning(f"Failed to validate token: {e}")
                self.__cache.delete("accessToken")

    def __mediaUserToken(self, fromLoop=False):
        if self.__config.get():
            logger.info("Checking media-user-token...")

            self.__session.headers.update(
                {
                    "media-user-token": self.__config.get()
                }
            )

            response = self.__session.get("https://amp-api.music.apple.com/v1/me/storefront")

            if response.status_code == 200:
                response = json.loads(response.text)

                self.storefront = response["data"][0].get("id")
                self.language = response["data"][0]["attributes"].get("defaultLanguageTag")

                self.__session.headers.update(
                    {
                        'accept-language': f'{self.language},en;q=0.9'
                    }
                )
            else:
                logger.error("Invalid media-user-token! Re-enter the token...")
                self.__config.delete()
                self.__config.set()
                self.__mediaUserToken(fromLoop=True)
        else:
            if not fromLoop:
                logger.error("Enter your media-user-token to continue!")
                self.__config.set()
            logger.info("Re-start the program...", 1)

    def __getErrors(self, errors):
        if not isinstance(errors, list):
            errors = [errors]
        for error in errors:
            err_status = error.get("status")
            err_detail = error.get("detail")
            logger.error(f"{err_status} - {err_detail}", 1)

    def __getJson(self):
        logger.info("Fetching api response...")

        cacheKey = f"{self.id}:{self.storefront}"
        __cache = self.__cache.get(cacheKey)
        if __cache:
            logger.info("Using the previous response found in cache...")
            return __cache

        apiUrl = f'https://amp-api.music.apple.com/v1/catalog/{self.storefront}/{self.kind}s/{self.id}'

        self.__session.params = {
            'include[songs]': 'albums,lyrics,syllable-lyrics',
            'l': f'{self.language}'
        }

        response = self.__session.get(apiUrl)
        response = json.loads(response.text)

        if not "errors" in response:
            self.__cache.set(cacheKey, response)
            return response
        else: self.__getErrors(response)

    def getInfo(self, url):
        self.__getUrl(url)

        if self.kind == "album":
            return album(
                self.__getJson(),
                syncpoints=self.sync,
            )
        elif self.kind == "song":
            return song(
                self.__getJson(),
                syncpoints=self.sync,
            )
        else:
            logger.error("Supports only albums and songs!", 1)