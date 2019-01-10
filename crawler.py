from time import sleep
from bs4 import BeautifulSoup

import urllib2
import validators
import threading

from bfs2 import Tree, Node
import editDistance as EditDistance

class Crawler:
    def __init__(self, url_set):
        self.tree = Tree(url_set)


    def crawl(self, depth, doPoliteness=False):
        # Fetch list of sites to crawl

        ## Repeat this ->
        # Choose one site to crawl
        while self.tree.depth < depth:
            node = self.tree.nextNode() # Set the node to the next in the frontier
            
            if node == None:
                return self.tree # If the frontier is empty => Return the tree
            
            self.updateNodeContentAndLink(node)

            #a = threading._start_new_thread(self.updateNodeContentAndLink(node), None)

            if doPoliteness:
                sleep(.5)

        return self.tree

    def updateNodeContentAndLink(self, node):
        next_site = node.data["url"]

        # Get site restrictions
        site_restrictions = self.getSiteRestrictions(next_site)

        source = ""

        # Push site links, if they are not restricted
        try:
            response = urllib2.urlopen(next_site)
            source = response.read()
        except urllib2.HTTPError:
            pass
                
        soup = BeautifulSoup(source, "html.parser")

        outgoing_links = set()
        ingoing_links = set()
        for link in soup.find_all('a'):
            try:
                #Identify outgoing links
                if validators.url(link.get("href")) == True:
                    outgoing_links.add(link.get("href"))
                else:
                    ingoing_links.add(link.get("href"))
            except TypeError:
                pass

        content = soup.get_text()

        node.data = {"url": next_site, "content": content}

        # Update sites_to_crawl
        final_links = outgoing_links - site_restrictions

        # Add to sites to crawl
        if node.depth == -1: # If the node is in a new layer => Update depths
            self.tree.depth += 1
            node.depth = self.tree.depth

        for link in final_links:
            newNode = Node(node, {"url": link, "content": ""}, self.tree.depth)
            node.children.append(newNode)
            self.tree.frontier.append(newNode)
        

    # Do edit distance on url_content_list
    def nearDuplicates(self, url_contents_list):
        content_list = url_contents_list

        # Iterate over each element in the list
        boundary = len(content_list)
        for i in range(0, boundary):
            # Check the edit distance on each element in the list
            for j in range(i+1, boundary):
                try:
                    # If doc1 and doc2 is >90% similar ? del from list : keep checking
                    if EditDistance.editDistance(content_list[i]["content"], content_list[j]["content"]) >= 0.9:
                        del content_list[i]
                        break
                    else:
                        pass
                except IndexError:
                    pass

        # Return new list
        return content_list

    def getSiteRestrictions(self, site):
        restrictions = set()
    
        # Get root of site
        site_split = site.split("/")
        root = ""
        if site_split[0] != "http:":
            return set()
        else:
            root = site_split[0] + "//" + site_split[2]
        
        try:
            # Find robot file
            response = urllib2.urlopen(root + "/robots.txt")
            robots_file = response.read()

            # Parse file for User-agent: * disallows ? Add to restrictions list : Pass the line
            addToRestrictions = False
            for line in robots_file.split("\n"):
                line_split = line.split(":")
                try:
                    if line_split[0] == "User-agent":
                        if line_split[1] == " *":
                            addToRestrictions = True
                        else:
                            addToRestrictions = False
                    else:
                        if addToRestrictions and validators.url(root + line_split[1].strip()) == True:
                            restrictions.add(root + line_split[1].strip())
                        else:
                            pass
                except IndexError:
                    pass
                except UnicodeDecodeError:
                    pass
        except urllib2.HTTPError:
            return set()

        # return set of all restrictions
        return restrictions



