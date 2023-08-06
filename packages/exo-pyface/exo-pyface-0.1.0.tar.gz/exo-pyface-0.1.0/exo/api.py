import requests
import json
import re


class exoREST:

    def __init__(self):
        self.url_list = {}

    def addAPI_URL(self, url_name, url):
        url_format = r"^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"

        if url == '':
            raise Exception('URL is null')
        if bool(re.match(url_format, url)) is False:
            raise Exception('URL format isn\'t matching')
        if url in self.url_list.values():
            raise Warning('URL already exists')
        if url_name == '':
            raise Exception('URL name can not be null')
        elif url_name in self.url_list.keys():
            raise Exception('URL name already exists')
        else:
            self.url_list[url_name] = url

    def getURL_LIST(self):
        return self.url_list

    def getDataFromAPI(self, url_name):
        if url_name not in self.url_list.keys():
            raise Exception('{} is not a valid urlname'.format(url_name))
        url = self.url_list[url_name]
        parsed = {}
        response = requests.get(url)
        # return response
        data = response.text
        # return data
        parsed = json.loads(data)
        return parsed
