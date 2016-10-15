from dbase.dataset import Dataset

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

class YouTube(Dataset):


    # Search youtube
    def search(self, qry):
        yt = build("youtube", "v3", developerKey=self._cfg.get("API KEYS", "google_key_api"))

        search_res = yt.search().list(
            q=qry,
            type="video",
            part="id,snippet",
            maxResults=10,
        ).execute()

        return search_res.get("items", [])

        # self._log.debug(search_res)
