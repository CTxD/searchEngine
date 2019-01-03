import json

import crawler as Crawler
import bfs as Bfs


# Set of urls, that we want to crawl
url_set = set()

# Import the urls from crawlLinks.json file
try:
    with open("crawlLinks.json", 'r') as inFile:
        data = json.load(inFile)
    
    for url in data["urls"]:
        url_set.add(url)
except:
    EnvironmentError("An error occured!")



# Init the crawler with the set of urls
crawler = Crawler.Crawler(url_set)
crawler_result = crawler.crawl(3, False)


next = crawler_result.next()
while next != None:
    print(next.data["url"])

    next = crawler_result.next()
