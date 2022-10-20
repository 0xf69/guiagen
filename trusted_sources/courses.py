#!/usr/bin/env python3

import re
import json
import requests


def udemy(keywords):
    url      = "https://www.udemy.com/api-2.0/search-courses/"
    headers  = {"Referer": "https://www.udemy.com/courses/search/"}

    return_data = []
    for keyword in keywords:
        params   = {"locale": "pt_BR", 'q': keyword}
        r        = requests.get(url, params=params, headers=headers)
        response = json.loads(r.text)
        
        courses  = response["courses"]
        
        for course in courses:
            return_data.append((course["title"],\
                        "https://www.udemy.com" + course["url"]))


    return return_data


def youtube(keywords):
    url = "https://www.youtube.com/results"

    return_data = []
    for keyword in keywords:
        params   = {"sp": "EgIQAw==", "search_query": keyword}
        r        = requests.get(url, params=params)
        response = r.text

        scraped_data = re.search("var ytInitialData = .*\;\<\/script\>", response)
        scraped_data = scraped_data.group()
        scraped_data = scraped_data[19:-10]
        scraped_data = json.loads(scraped_data)

        contents = scraped_data["contents"]
        contents = contents["twoColumnSearchResultsRenderer"]
        contents = contents["primaryContents"]
        contents = contents["sectionListRenderer"]
        contents = contents["contents"][0]
        contents = contents["itemSectionRenderer"]
        contents = contents["contents"][1::]

        for content in contents:
            content     = content["playlistRenderer"]
            title       = content["title"]["simpleText"]
            playlist_id = content["playlistId"]

            url_return         = f"https://www.youtube.com/playlist?list={playlist_id}"
            
            return_data.append((title, url_return))

    
    return return_data


print(youtube("c++"))