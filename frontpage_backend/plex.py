import json, pycurl
from io import BytesIO
from bs4 import BeautifulSoup

class Plex():

    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.reply = {}

    def __apicall(self, host, port, endpoint):
        buffer = BytesIO()
        c = pycurl.Curl()

        header = [
            'Content-Type: application/xml; charset=utf-8',
            'Content-Length: 0',
            'X-Plex-Product: YTB-SSO',
            'X-Plex-Version: v2.0',
        ]

        url = 'http://' + host + ':' + port + endpoint

        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.HTTPHEADER, header)

        c.setopt(pycurl.TIMEOUT, 10)
        c.setopt(c.WRITEDATA, buffer)

        try:
            c.perform()
            c.close()
        except pycurl.error:
            return 'Failed communicating with Plex.'

        try:
            return buffer.getvalue().decode('utf-8')
        except json.JSONDecodeError:
            return 'JSON API failure'

    def search_for_movie(self, title, date):
        request = self.__apicall(self.__host, self.__port, '/search?query=' + title.replace(' ', '%20'))

        body = BeautifulSoup(request, 'html.parser')
        match = False

        year = date.split('-')[0]

        for video in body.mediacontainer.findAll('video'):
            if video['title'] == title and video['year'] == year and video['type'] == 'movie':
                match = True

        return match

    def search_for_show(self, title, date):
        request = self.__apicall(self.__host, self.__port, '/search?query=' + title.replace(' ', '%20'))

        body = BeautifulSoup(request, 'html.parser')
        match = False

        year = date.split('-')[0]

        for video in body.mediacontainer.findAll('video'):
            if video['title'] == title and video['year'] == year and video['type'] == 'show':
                match = True

        return match