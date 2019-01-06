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
crawler_result = crawler.crawl(2, False)

saveData = list()

next = crawler_result.next()
while next != None:
    print(next.data["url"])

    saveData.append({"url": next.data["url"], "content": next.data["content"]})

    next = crawler_result.next()

print("Crawling done!\nDumping to crawlContent.json...")

try:
    with open("crawlContent.json", 'wb') as outFile:
        json.dump(saveData, outFile)
        outFile.truncate()
except:
    pass

print("Saved successfully!")