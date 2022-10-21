#!/usr/bin/env python3

import sys
import random
from time import time
from trusted_sources import books, courses


def search():
    keywords_book   = input("> Books keywords: ")
    keywords_book   = keywords_book.split(',')

    keywords_course = input("> Course keywords: ")
    keywords_course = keywords_course.split(',')

    db_books   = []
    print("[+] searching books")
    print("[+] querying zlibrary")
    db_books   += books.zlib(keywords_book)
    print("[+] querying google books")
    db_books   += books.google(keywords_book)

    print()
    db_courses = []
    print("[+] searching courses")
    print("[+] querying udemy")
    db_courses   += courses.udemy(keywords_course)

    if ("-y" in sys.argv) or ("--youtube" in sys.argv):
        print("[+] querying youtube")
        db_courses += courses.youtube(keywords_course)

    print()
    
    keywords_by_space = keywords_course + keywords_book
    keywords_by_space = " ".join(keywords_by_space)
    keywords_by_space = keywords_by_space.split()
    keywords_by_space = set(keywords_by_space)

    if ("-f" in sys.argv) or ("--filter" in sys.argv):
        db_books   = filter(keywords_by_space, db_books)
        db_courses = filter(keywords_by_space, db_courses)


    return_data = {"books": db_books, "courses": db_courses}
    return return_data
    

def filter(keywords, db):
    index = 0
    db2 = []
    for course in db:
        name = course[0]
        name = name.lower()

        for keyword in keywords:
            keyword = keyword.lower()
            if keyword in name:
                db2.append(course)
                break
    
        index += 1

    items = []
    names = []
    for item in db2:
        name = item[0]
        if name not in names:
            items.append(item)
            names.append(name)

    items_amount = random.randint(1, len(items))
    items        = random.sample(items, items_amount)
    
    return items


def generate_markdown(data):
    topic   = data["topic"]
    books   = data["books"]
    courses = data["courses"]
    
    with open("./TEMPLATE.md", 'r') as f:
        template = f.read()

    template  = template.format(topic, topic)
    template += generate_subtopic("cursos", courses)
    template += generate_subtopic("livros", books)


    return template


def generate_subtopic(subtopic, format):
    emoji_pool = ['📮', '📕', '💼', '🎙', '📮']
    emoji      = random.choice(emoji_pool)
    template   = f"\n## {emoji} {subtopic.title()}\n"

    for media in format:
        name = media[0]
        url  = media[1]
        line = f"* [{name}]({url})\n"

        template += line

    return template
        


def main():
    topic = input("> topic: ")
    topic = topic.title()

    data          = search()
    data["topic"] = topic

    markdown      = generate_markdown(data)

    if ("-s" in sys.argv) or ("--save" in sys.argv):
        filename = f"{topic}-{int(time())}.md"
        filename = filename.replace(' ', '_')

        with open(filename, "x") as f:
            f.write(markdown)
    
        print(f"[+] writed markdown to {filename}")
    else:
        print(markdown)


main()
