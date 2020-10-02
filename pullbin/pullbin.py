from enum import Enum
from bs4 import BeautifulSoup
from datetime import datetime

from pullbin.utils import parse_extension

import requests, os, re

class Pullbin:
    class ResponseType(Enum):
        IsFilePath = 1
        IsDirPath = 2

    class DomainType:
        paste = 'pastebin'
        ghost = 'ghostbin'
        _all = r'({paste}|{ghost})'.format(paste=paste, ghost=ghost)

    def __init__(self):
        self.domain = 'pastebin'
        self.url = None
        self.key = None
        self.request = None
        self.fullpath = None
        self.content = None

    @staticmethod
    def _show():
        print(f"""
                     _ _ _     _       
         _ __  _   _| | | |__ (_)_ __  
        | '_ \| | | | | | '_ \| | '_ \ 
        | |_) | |_| | | | |_) | | | | |
        | .__/ \__,_|_|_|_.__/|_|_| |_|
        |_|
                #created by santosr@2017-{datetime.now().year}
                
        """)

    def _make_url(self):
        if self.domain == self.DomainType.paste:
            return "https://pastebin.com/{key}".format(key=self.key)
        elif self.domain == self.DomainType.ghost:
            return "https://ghostbin.co/paste/{key}".format(key=self.key)

    def set_domain(self, domain):
        self.domain = domain

    def set_path(self, path):
        responseType = None

        if os.path.isfile(os.path.expandvars(path)):
            self.fullpath = path
            responseType = self.ResponseType.IsFilePath
        elif os.path.isdir(os.path.expandvars(path)):
            self.fullpath = path
            responseType = self.ResponseType.IsDirPath
        elif os.path.exists(os.path.expandvars(path)):
            raise Exception(f"{path} file exist")

        return responseType
    
    def set_filename(self, filename):
        self.fullpath = '{}/{}'.format(self.fullpath,filename)

    def check_domain(self, domain):
        valid = re.match(self.DomainType._all, domain)
        if not valid:
            raise Exception(f"{domain} not exist")
        
        return valid

    def check_key(self, key):
        self.key = key
        self.url = self._make_url()
        self.request = requests.get(self.url)
        self.request.raise_for_status()
        status_code = self.request.status_code
        if status_code == 200:
            return True
        else:
            raise Exception(f"Check key unknow error. status_code({status_code})")

    def get_current_path(self):
        return os.path.dirname(os.path.realpath(__name__))

    def scrap_content(self):
        soup = BeautifulSoup(self.request.text, 'html.parser')
        if self.domain == self.DomainType.paste:
            self.content = soup.find("textarea", {"id": "paste_code"})
        elif self.domain == self.DomainType.ghost:
            self.content = soup.find("div", {"id": "code"})
        else:
            raise Exception(f"Unknow domain {self.domain}")

    def _scrap_file_extension(self):
        soup = BeautifulSoup(self.request.text, 'html.parser')
        if self.domain == self.DomainType.paste:
            return soup.find("div", {"id": "code_buttons"}).find("span", {"class": "h_640"}).a.text
        elif self.domain == self.DomainType.ghost:
            return soup.find("span", {"class": "paste-subtitle"}).text.rstrip()

    def _validate_extension(self, extension):
        return parse_extension(extension)

    def write(self):
        extension = self._validate_extension(self._scrap_file_extension())
        self.fullpath = f'{self.fullpath}.{extension}'
        with open(self.fullpath, 'w+') as file:
            file.write(self.content.get_text())
        self.close()

    def close(self):
        self.request.close()
