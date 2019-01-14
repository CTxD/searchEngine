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
crawlResult = crawler.crawl(50, False)

print("Crawling done!\nDumping to crawlContent.json...")

saveData = []

for child in crawlResult.visitedNodes():
    saveData.append(child.data) # Dump to save object

bLen = len(saveData)

print("Save Data loaded!\nChecking for duplicates...")
saveData = crawler.nearDuplicates(saveData)

print("Duplicates found: " + str(bLen - len(saveData)))

try:
    with open("crawlContent.json", 'wb') as outFile:
        json.dump(saveData, outFile)
except:
    EnvironmentError("Save content could not be saved")

print("Saved successfully!")
print("Number of pages: " + str(len(saveData)))