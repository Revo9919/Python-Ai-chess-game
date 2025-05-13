class Node(object):
    def __init__(self, data):
        self.data = data #
        self.children = [] #array of possible moves from that move
        self.leaf = True

    #appends to the self.children
    def add_child(self, obj):
        self.children.append(obj)


    #sets self.leaf to false if node has children
    def setIsLeaf(self):
        if len(self.children) > 0:
            self.leaf = False

    #returns whether self.leaf is false or true
    def getIsLeaf(self):
        return self.leaf




