class AVL_Node:
    def __init__(self, x, y, z, dimension=1):
        self.x = x
        self.y = y
        self.z = z
        self.parent = None
        self.left = None
        self.right = None
        self.successor = None  # next greater value
        self.predecessor = None  # previous equal or lesser value
        self.second_dim_tree = None
        self.dimension = dimension

    def __str__(self):  # pretty print the node
        if self.dimension is 1:
            return "{X= " + str(self.x) + ", Y= " + str(self.y) + ", Z= " + str(self.z) + "}"
        elif self.dimension is 2:
            return "{Y= " + str(self.y) + ", X= " + str(self.x) + ", Z= " + str(self.z) + "}"
        else:
            return "{Z= " + str(self.z) + ", Y= " + str(self.y) + ", X= " + str(self.x) + "}"

    def find(self, k, next=False):
        # next is a boolean variable, used for range_query, in case the lower bound isn't found
        if k == self.x:
            return self
        elif k <= self.x:
            if not self.left:
                if next is False:
                    return None
                else:
                    return self
            else:
                return self.left.find(k, next)
        else:
            if not self.right:
                if next is False:
                    return None
                else:
                    return self
            else:
                return self.right.find(k, next)

    def find_max(self):  # Finds max value in tree and returns its node
        current = self
        while current.right:
            current = current.right
        return current

    def find_predecessor(self):  # Finds predecessor of a given node
        if self.left:
            return self.left.find_max()

    def insert(self, node):
        if node is None:
            return

        '''second_dim_node has to be different in each insertion because it is 
        being inserted on a different tree every time. Therefore, it has different predecessors,
        different successors, different parent, different children.
        '''
        if node.x <= self.x:
            if self.left is None:
                self.left = node
                node.parent = self

                node.successor = self
                if self.predecessor:
                    node.predecessor = self.predecessor
                    self.predecessor.successor = node
                self.predecessor = node

            else:
                self.left.insert(node)
        else:
            if self.right is None:
                self.right = node
                node.parent = self

                node.predecessor = self
                if self.successor:
                    node.successor = self.successor
                    self.successor.predecessor = node
                self.successor = node

            else:
                self.right.insert(node)

        # 2nd Dimension Stuff
        if self.dimension is 1:
            second_dim_node = AVL_Node(node.y, node.x, node.z, 2)
            self.second_dim_tree.insert(second_dim_node)

    def delete(self):
        if self.left is None or self.right is None:
            if self is self.parent.left:
                self.parent.left = self.left or self.right
                if self.parent.left:
                    self.parent.left.parent = self.parent
            else:
                self.parent.right = self.left or self.right
                if self.parent.right:
                    self.parent.right.parent = self.parent
            return self
        else:
            s = self.find_predecessor()
            self.x, s.x = s.x, self.x
            return s.delete()

    def range_query(self, lower, upper):  # lower limit, upper limit
        head = self.find(lower, True)  # head of the list
        results = [head]  # list of results, insert first element
        while results[-1].successor and results[-1].successor.x <= upper:  # successor of last element exists
            results.append(results[-1].successor)
        return results


def height(node):  # height of this node
    if node is None:
        return -1
    else:
        return node.height


def update_height(node):  #
    node.height = max(height(node.left), height(node.right)) + 1