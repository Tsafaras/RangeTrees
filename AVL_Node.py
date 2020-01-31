def purge(min_node, max_node):
    if min_node <= max_node:
        results = [min_node]  # head of the list
        while results[-1].successor and results[-1].successor <= max_node:
            # successor of last element exists
            results.append(results[-1].successor)
    else:
        results = [max_node]  # head of the list
        while results[-1].predecessor and results[-1].predecessor >= min_node:
            # predecessor of last element exists
            results.append(results[-1].predecessor)
    return results


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
        self.higher_dim_tree = None
        self.dimension = dimension
        self.height = 1
        self.balance = 0

    # ---------------------------- Overloaded operators ----------------------------
    def __str__(self):  # pretty print the node
        if self.dimension is 1:
            return "{X= " + str(self.x) + ", Y= " + str(self.y) + ", Z= " + str(self.z) + "}"
        elif self.dimension is 2:
            return "{Y= " + str(self.x) + ", X= " + str(self.y) + ", Z= " + str(self.z) + "}"
        else:
            return "{Z= " + str(self.x) + ", Y= " + str(self.y) + ", X= " + str(self.z) + "}"

    def __eq__(self, other):
        return self.x is other.x and self.y is other.y and self.z is other.z

    def __le__(self, other):
        return self.x <= other.x

    def __ge__(self, other):
        return self.x >= other.x

    # ---------------------------- Functions ----------------------------

    def find(self, k, next=False):
        # next is a boolean variable, used for range_query, in case the x_low bound isn't found
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

    def find_min(self):
        current = self
        while current.left:
            current = current.left
        return current

    def insert(self, node):
        if node is None:
            return

        '''higher_dim_node has to be different in each insertion because it is 
        being inserted on a different tree every time.
        It must have (if any) different:
        predecessor, successor, parent, children.
        '''
        if node <= self:
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
            higher_dim_node = AVL_Node(node.y, node.x, node.z, 2)
            self.higher_dim_tree.insert(higher_dim_node)

    def delete(self):
        if self.left is None or self.right is None:
            if self is self.parent.left:
                self.parent.left = self.left or self.right
                self.parent.predecessor = self.left or self.right
                if self.parent.left:
                    self.parent.left.parent = self.parent
                    self.parent.left.successor = self.parent
            else:
                self.parent.right = self.left or self.right
                self.parent.successor = self.left or self.right
                if self.parent.right:
                    self.parent.right.parent = self.parent
                    self.parent.right.successor = self.parent
            return self
        else:
            s = self.predecessor
            self.swap(s)

            return s.delete()

    def range_query(self, x_low, x_high, y_low, y_high):  # x_low limit, x_high limit
        head = self.find(x_low, True)  # head of the list
        results = [head]  # list of results, insert first element
        while results[-1].successor and results[-1].successor.x <= x_high:
            # successor of last element exists
            results.append(results[-1].successor)
        return results

    # left - right logic, updates the node's height and balance factor
    def update(self):
        if self.left:
            if self.right:
                self.height = max(self.left.height, self.right.height) + 1
                self.balance = self.left.height - self.right.height
            else:
                self.height = self.left.height + 1
                self.balance = self.left.height
        elif self.right:
            self.height = self.right.height + 1
            self.balance = -self.right.height
        else:
            self.height = 1
            self.balance = 0

    def swap(self, s):
        self.x, s.x = s.x, self.x
        self.y, s.y = s.y, self.y
        self.z, s.z = s.z, self.z
