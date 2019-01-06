from copy import copy

class Tree:
    def __init__(self, urlList):
        # Initialize the root of the tree and the depth
        self.root = Node(None, "root")
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

class Node:
    def __init__(self, parent, data, depth=-1):
        self.parent = parent
        self.data = data
        self.children = []
        self.depth=-1

tree = Tree([])

r = Node(tree.root, "r")
n1 = Node(r, "n1")
n2 = Node(n1, "n2")
n3 = Node(n2, "n3")
n4 = Node(n3, "n4")

tree.root.children.append(r)
r.children.append(n1)
n1.children.append(n2)
n2.children.append(n3)
n3.children.append(n4)

print("D:")
for child in n3.children:
    print("CD:", child.data)