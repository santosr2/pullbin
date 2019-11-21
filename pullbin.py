#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
    #       PULLBIN.py
    #
    #  author: Rubens Santos <me[at]z1ron>
    #  description: this script does web scraping on the domains pastebin and ghostbin and writes to files
    #  license: MIT
    #  version: 1.0.1
    #  contact: submit your issue
    #  pullbin@2017
    #
    
'''


import requests
import re
import sys
from bs4 import BeautifulSoup

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def pullbin():
    print(bcolors.HEADER+bcolors.BOLD+'''
                 _ _ _     _       
     _ __  _   _| | | |__ (_)_ __  
    | '_ \| | | | | | '_ \| | '_ \ 
    | |_) | |_| | | | |_) | | | | |
    | .__/ \__,_|_|_|_.__/|_|_| |_|
    |_|
            #created by z1ron@2017
            
    '''+bcolors.ENDC)                            

#howto
def usage():
    print(bcolors.BOLD+'''
        http[s]://www.pastebin.com/KEY
     OR
        http[s]://www.ghostbin.com/KEY
    '''+bcolors.ENDC)

# this function checks if the link is valid
def verify_link(LINK):
    print('[#]:~ Analyzing link, Wait a minute ...')
    status = requests.get(LINK).status_code
    if(status == 200): return 1 # true
    else: return status
            

# main
pullbin() # pullbin text

RegDOMAIN = '(http|https)\:\/{2}(pastebin|ghostbin)\.com' # regexp domains link

LINK = raw_input(bcolors.BOLD+"[#]:~ Insert the page link: "+bcolors.ENDC)

DOMAIN = 'pastebin' # default domain
if(DOMAIN not in LINK): DOMAIN = 'ghostbin'

print # new line

if(re.match(RegDOMAIN, LINK) != None):
    status = verify_link(LINK)
    if(status == 1):
        print(bcolors.OKBLUE+'[#]:~ Successful analysis'+bcolors.ENDC)
        print('[#]:~ Capturing HTML')
        SITE = requests.get(LINK)
        pathfile = raw_input(bcolors.BOLD+"\n[#]:~ Enter the path with filename: "+bcolors.ENDC)
        print # new line
        print('[#]:~ Processing HTML page')
        soup = BeautifulSoup(SITE.text,'html.parser') # get all page html
        if(DOMAIN == 'pastebin'): html = soup.find("textarea") # getting only textarea tag
        else: html = soup.find("div",{'id': 'code'}) #getting only div#code tag
        print("[#]:~ Getting tag content")
        text = ''.join(html.get_text()).encode('utf-8')
        print("[#]:~ Creating file")
        try: # check if file exists
            with open(pathfile, 'w+') as arq:
                print('[#]:~ Writing file')
                arq.write(text)
                arq.close()
                print(bcolors.OKGREEN+bcolors.BOLD+"[#]:~ Successful process"+bcolors.ENDC)
                print # new line
        except IOError:
                print(bcolors.WARNING+bcolors.BOLD+'[#]:~ Error, can\'t create file!'+bcolors.ENDC)
                sys.exit(1)
    else: # status code http
        print(bcolors.FAIL+"[#]:~ Error: "+str(status)+" status code"+bcolors.ENDC)
else:
    print(bcolors.FAIL+bcolors.BOLD+"\n[#]:~ Only the Pastebin and Ghostbin domains"+bcolors.ENDC)
    usage()
# end main
