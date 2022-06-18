#!/usr/bin/env python3

import json
import requests
from discord import Embed

data = json.load(open('config.json'))

class Photo :
    def __init__(self) :
        self.url = []
        self.download = []
        self.description = []
        self.alt_description = []
        self.author = []
        self.page = 0
    def setPhotoRandom(self) -> None:
        apiKey = data['API_KEY']
        rq = requests.get(f"https://api.unsplash.com/photos/random?client_id={apiKey}&orientation=landscape")
        self.url.append(rq.json()['urls']['regular'])
        self.download.append(rq.json()['links']['download'])
        self.description.append(rq.json()['description'])
        self.alt_description.append(rq.json()['alt_description'])
        self.author.append(rq.json()['user']['username'])
    def setPhotoFromSearch(self, search) -> None:
        apiKey = data['API_KEY']
        rq = requests.get(f"https://api.unsplash.com/search/photos/?query={search}&client_id={apiKey}&orientation=landscape")
        for photo in rq.json()['results']:
            self.url.append(photo['urls']['regular'])
            self.download.append(photo['links']['download'])
            self.description.append(photo['description'])
            self.alt_description.append(photo['alt_description'])
            self.author.append(photo['user']['username'])
    def getEmbedPhotoFromPage(self, page) -> Embed:
        if self.description[page] != None and len(self.description[page]) > 256 :
            description = self.description[page][:250] + "..."
        else :
            description = self.description[page]
        embed = Embed(title=description, description=self.alt_description[page], color=0x2f1376)
        embed.set_image(url=self.url[page])
        embed.add_field(name="Author", value=self.author[page], inline=False)
        embed.set_footer(text=f"Page {page + 1} / {len(self.url)}")
        return (embed)
    def getPage(self) -> int:
        return (self.page)
    def setPage(self, page) -> None:
        self.page = page


def getDataFromId(photo_data, message_id) -> Photo:
    for data in photo_data:
        if data['message_id'] == message_id:
            return (data['photo'])
    return (None)