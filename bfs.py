class Tree:
    def __init__(self):
        self.frontier = list()
        self.lastNodes = list()

        self.root = Node(None, None)
        self.frontier.append(self.root)

        self.depth = 0

    def next(self):
        # Retrieve next node
        if self.frontier:
            return_node = self.frontier[0]
            del self.frontier[0]

            self.lastNodes.append(return_node)
                
            return return_node
        else:
            # If frontier is empty ? update frontier : return None
            if self.lastNodes:
                for child in self.lastNodes:
                    if child.children:
                        for node in child.children:
                            self.frontier.append(node)

                        self.depth += 1
                        self.lastNodes = list()

                        return self.next()
                    else:
                        return None
            else:
                return None

    
class Node:
    def __init__(self, parent, data):
        self.parent = parent
        self.children = list()
        self.data = data
        self.visited = False

    def appendChild(self, node):
        self.children.append(node)

