import os
from bdownload import BDownloader, download

import logging
logger = logging.getLogger(__name__)
if (logger.hasHandlers()):
    logger.handlers.clear()
logging.basicConfig(filename = "app.log", level = logging.DEBUG)


class TestBDownloader():
    def __init__(self):
        self.temp_dir = "Temp/"

    def test_bdownloader_downloads(self, url, file_name):
        """
            `file`:location to be stored
            `url`:source url to be downloaed
        """
        files = [
            {
                "file": os.path.join(self.temp_dir, file_name),
                "url": url,
            }
        ]

        file_urls = [(f["file"], f["url"]) for f in files]
        try:
            with BDownloader(max_workers=40, progress='milli') as downloader:
                downloader.downloads(file_urls)
                downloader.wait_for_all()
        except Exception as E:
            logging.error("Error 500: Internal Server Error : %s", str(E))
            return str(E), 500