import crawler as Crawler
import bfs as Bfs

url_set = set()
url_set.add("http://www.google.dk/")
url_set.add("http://www.facebook.com/")
url_set.add("https://stackoverflow.com/")


crawler = Crawler.Crawler(url_set)
crawler_result = crawler.crawl(6, False)

next = crawler_result.next()
while next != None:
    print(next.data["url"])

    next = crawler_result.next()
