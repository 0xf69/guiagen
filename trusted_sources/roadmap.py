#!/usr/bin/env python3

import re
import requests


def google(keyword):
    keywords = keyword.split()
    keyword  = ""

    for keywd in keywords:
        keyword += '"' + keywd + "\" "
    keyword  += "\"roadmap\""


    url      = "https://www.google.com/search"
    headers  = {"Host": "Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0"}
    params   = {"tbm": "isch", 'q': keyword, 'oq': keyword}

    r        = requests.get(url, params=params)
    response = r.text

    print(response)
    data_id  = re.search("Image Results\<\/h2\>\<div.*?data-id=\"(.*?)\"", response)
    
    print(data_id.groups())


google("nuclear bomb")
