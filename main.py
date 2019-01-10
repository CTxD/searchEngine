import json

from crawler import Crawler

# Set of urls, that we want to crawl
urlSet = set()

# Import the urls from crawlLinks.json file
try:
    with open("crawlLinks.json", 'r') as inFile:
        data = json.load(inFile)
    
    for url in data["urls"]:
        urlSet.add(url)
except:
    EnvironmentError("crawlLinks.json could not be loaded")

# Init the crawler with the set of urls
crawler = Crawler(urlSet)
crawlResult = crawler.crawl(20, False)

print("Crawling done!\nDumping to crawlContent.json...")

saveData = []

for child in crawlResult.visitedNodes():
    print(child.data["url"])
    saveData.append(child.data) # Dump to save object

try:
    with open("crawlContent.json", 'wb') as outFile:
        json.dump(saveData, outFile)
except:
    EnvironmentError("Save content could not be saved")

print("Saved successfully!")
print(len(saveData))