import crawler as Crawler
import bfs as Bfs

# Set of urls, that we want to crawl
url_set = set()
url_set.add("http://www.google.dk/")
url_set.add("http://www.facebook.com/")
url_set.add("https://stackoverflow.com/")

# Init the crawler with the set of urls
crawler = Crawler.Crawler(url_set)
crawler_result = crawler.crawl(2, False)


next = crawler_result.next()
while next != None:
    print(next.data["url"])

    next = crawler_result.next()

for node in crawler_result.root.children:
    print(node.data["content"])