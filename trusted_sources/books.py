#!/usr/bin/env python3

import re
import requests

def google(keywords):
    url        = "https://www.google.com/search"
    headers    = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0"}

    return_data = []
    for keyword in keywords:
        params   = {"tbm": "bks", 'q': keyword}
        r        = requests.get(url, headers=headers, params=params)
        response = r.text

        response = re.findall("\<a href=\"https://books\.google\.com/books\?id=.*?\"\>\<br\>\<h3 .*?\<\/h3\>", response)

        for content in response:
            url_return   = re.search("\<a href=\"https://books.google.com\/books\?id=(.*?)&", content)
            url_return   = url.group(1)
            url_return   = f"https://www.google.com.br/books/edition/_/{url}" 

            title = re.search("\<h3 class=\".*?\"\>(.*?)\<\/h3\>", content)
            title = title.group(1)

            if title.endswith("..."):
                title = title[0:-3:]

            return_data.append((title, url))


    return return_data


def zlib(keywords):
    url = "https://b-ok.lat/s/"

    return_data = []
    for keyword in keywords:
        r        = requests.get(url + keyword)
        response = r.text
        response = re.findall("\<a href=\"(\/book/.*?)\" style=.*?\"\>(.*?)\<\/a>", response)
        
        for content in response:
            url_return   = "https://b-ok.lat" + content[0]
            title = content[1]

            return_data.append((title, url_return))


    return return_data


print(zlib(["python", "c++"]))