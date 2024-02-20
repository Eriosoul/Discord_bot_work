import requests
import os
import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup


class HockeyTeams:
    def __init__(self):
        load_dotenv()
        self.url = os.getenv("LINK")
        self.s = requests.Session()
    def gettitle(self, x):
        new_url =f"{self.url}?page_num={x}"
        r = requests.get(new_url)
        sp = BeautifulSoup(r.text, 'html.parser')
        print(sp.title.text)
        return

    def gettitle_session(self, x):
        new_url =f"{self.url}?page_num={x}"
        r = self.s.get(new_url)
        sp = BeautifulSoup(r.text, 'html.parser')
        print(sp.title.text)
        return

    def main(self):
        # no session 0:00:07.966700
        print("no sesion")
        start = datetime.datetime.now()
        for x in range(1, 21):
            self.gettitle(x)
        finish = datetime.datetime.now() - start
        print(finish)
        # with session 0:00:07.170145
        print("sesion")
        start = datetime.datetime.now()
        for x in range(1, 21):
            self.gettitle_session(x)
        finish = datetime.datetime.now() - start
        print(finish)
