def purge(min_node, max_node):
    results = [min_node]  # head of the list
    successor = min_node.next_larger()
    while successor and successor <= max_node:
        # successor of last element exists
        results.append(successor)
        successor = successor.next_larger()
    return results


class leaf:
    def __init__(self, x, y, z, parent):
        self.x = x
        self.y = y
        self.z = z
        self.parent = parent
        self.predecessor = None
        self.successor = None

    def __str__(self):
        if self.parent.dimension is 1:
            return "{X= " + str(self.x) + ", Y= " + str(self.y) + ", Z= " + str(self.z) + "}"
        elif self.parent.dimension is 2:
            return "{Y= " + str(self.x) + ", X= " + str(self.y) + ", Z= " + str(self.z) + "}"
        else:
            return "{Z= " + str(self.x) + ", Y= " + str(self.y) + ", X= " + str(self.z) + "}"

    def delete(self):
        if self.predecessor and self.successor:
            self.predecessor.successor = self.successor
            self.successor.predecessor = self.predecessor
        elif self.predecessor:
            self.predecessor.successor = None
        elif self.successor:
            self.successor.predecessor = None

        if self is self.parent.left_leaf:
            self.parent.left_leaf = None
        else:
            self.parent.right_leaf = None

class AVL_Node:
    def __init__(self, x, y, z, dimension=1):
        self.x = x
        self.y = y
        self.z = z
        self.parent = None
        self.left = None
        self.right = None
        self.higher_dim_tree = None
        self.dimension = dimension
        self.height = 1
        self.balance = 0
        self.left_leaf = leaf(x, y, z, self)
        self.right_leaf = None

    # ---------------------------- Overloaded operators ----------------------------
    def __str__(self):  # pretty print the node
        if self.dimension is 1:
            return "{X= " + str(self.x) + ", Y= " + str(self.y) + ", Z= " + str(self.z) + "}"
        elif self.dimension is 2:
            return "{Y= " + str(self.x) + ", X= " + str(self.y) + ", Z= " + str(self.z) + "}"
        else:
            return "{Z= " + str(self.x) + ", Y= " + str(self.y) + ", X= " + str(self.z) + "}"

    def __eq__(self, other):
        if other:
            return self.x is other.x and self.y is other.y and self.z is other.z
        else:
            return False

    def __le__(self, other):
        return self.x <= other.x

    def __ge__(self, other):
        return self.x >= other.x

    # ---------------------------- Functions ----------------------------

    def find(self, k, next=False):
        # next is a boolean variable, used for range_query, in case the low bound isn't found
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

    def next_larger(self):
        if self.right:
            return self.right.find_min()
        current = self
        while current.parent and current is current.parent.right:
            current = current.parent
        return current.parent

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
        parent, children.
        '''
        if node <= self:
            if self.left is None:
                self.left = node
                node.parent = self

                self.fix_left_leaf(node)
            else:
                self.left.insert(node)
        else:
            if self.right is None:
                self.right = node
                node.parent = self
                self.fix_right_leaf(node)
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
                if self.parent.left:
                    self.parent.left.parent = self.parent
            else:
                self.parent.right = self.left or self.right
                if self.parent.right:
                    self.parent.right.parent = self.parent
            if self.right_leaf:
                self.parent.left_leaf = self.right_leaf
                self.parent.left_leaf.parent = self.parent
                self.right_leaf = None
            return self
        else:
            s = self.next_larger()
            self.swap(s)
            if s.right_leaf:
                s.parent.left_leaf = s.right_leaf
                s.right_leaf.parent = s.parent
                s.right_leaf = None
            place = self.left.find_max()
            place.right_leaf = s.left_leaf
            place.right_leaf.parent = place
            s.left_leaf = None
            return s.delete()

    def find_split(self, low, high):
        x = self.x
        if self.x is low or self.x is high:
            return self
        elif self.x < low:
            if self.x > high:
                return self
            else:
                split_node = self.right.find_split(low, high)
        elif self.x < high:
            return self
        else:
            split_node = self.left.find_split(low, high)
        return split_node

    def range_query(self, x_low, x_high, y_low, y_high):  # x_low limit, x_high limit

        node = self.find_split(x_low, x_high)
        if node is None:
            return

        node = node.higher_dim_tree.root.find(y_low, True)
        if node.y < x_low:
            return

        results = [node]
        while node.successor and node.successor.x <= y_high:
            # successor of last element exists and is within range
            if x_low <= node.successor.y <= x_high:
                results.append(node.successor)
            node = node.successor

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

    def fix_left_leaf(self, node):
        node.right_leaf = self.left_leaf
        node.right_leaf.parent = node
        if node.right_leaf.predecessor:
            node.right_leaf.predecessor.successor = node.left_leaf
            node.left_leaf.predecessor = node.right_leaf.predecessor
        node.left_leaf.successor = node.right_leaf
        node.right_leaf.predecessor = node.left_leaf
        self.left_leaf = None

    def fix_right_leaf(self, node):
        if self.right_leaf:
            node.right_leaf = self.right_leaf
            node.right_leaf.parent = node
            if node.right_leaf.predecessor:
                node.right_leaf.predecessor.successor = node.left_leaf
                node.left_leaf.predecessor = node.right_leaf.predecessor
            node.left_leaf.successor = node.right_leaf
            node.right_leaf.predecessor = node.left_leaf
            self.right_leaf = None
        else:
            previous = self.left_leaf or self.left.find_max_leaf()
            if previous.successor:
                previous.successor.predecessor = node.left_leaf
                node.left_leaf.successor = previous.successor
            previous.successor = node.left_leaf
            node.left_leaf.predecessor = previous

    def find_max_leaf(self):
        candidate = self.find_max()
        return candidate.right_leaf or candidate.left_leaf

    def find_leaf(self, k):
        if k > self.x:
            return self.right_leaf or self.right.find_leaf(k)
        else:
            return self.left_leaf or self.left.find_leaf(k)