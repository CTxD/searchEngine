from copy import copy

class Tree:
    def __init__(self, urlList):
        # Initialize the root of the tree and the depth
        self.root = Node(None, {"url": "root", "content": "root"}, 0)
        self.depth = 1
        
        # Initialize frontier
        self.frontier = []

        # First depth is set to the input urlList
        for url in urlList:
            nodeRef = Node(self.root, {"url": url, "content": ""}, self.depth) # Init the data with url and empty content

            # Let the frontier hold the layer too
            self.frontier.append(nodeRef)
            self.root.children.append(nodeRef)

    # Return the next frontier node
    def nextNode(self):
        if self.frontier:
            returnNode = self.frontier[0]
            del self.frontier[0]

            return returnNode
        else:
            return None

    def visitedNodes(self):
        print(self.depth)
        returnList = []
        returnList.append(self.root)
        
        i = 0
        try:
            while self.frontier[i].depth < self.depth:
                for child in returnList[i].children: 
                    if child.data["content"] == "": # Check if node is valid
                        pass
                    
                    returnList.append(child) # Append node to end of returnList

                i += 1 # Increment node
        except IndexError:
            pass

        return returnList

class Node:
    def __init__(self, parent, data, depth=-1):
        self.parent = parent
        self.data = data
        self.children = []
        self.depth=-1