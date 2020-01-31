from sortedcontainers import SortedList


class leaf:
    def __init__(self, x, y, z, parent=None):
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

    def __lt__(self, other):
        return self.x < other.x

    def __eq__(self, other):
        if other:
            return self.x is other.x and self.y is other.y and self.z is other.z
        else:
            return False

    def __le__(self, other):
        return self.x <= other.x

    def __ge__(self, other):
        return self.x >= other.x


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
        if dimension is 1:
            self.left_leaf = leaf(x, y, z, self)
        else:
            self.left_leaf = None
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

    def find_predecessor(self):
        if self.left:
            return self.left.find_max()
        current = self
        while current.parent and current is current.parent.left:
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

                if self.dimension is 1:
                    self.fix_left_leaf(node)
            else:
                self.left.insert(node)
        else:
            if self.right is None:
                self.right = node
                node.parent = self

                if self.dimension is 1:
                    self.fix_right_leaf(node)
            else:
                self.right.insert(node)

    # left - right logic, updates the node's height and its balance factor
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

    def inorder_attach(self, k):
        # First recur on left child
        if self.left:
            if self.left.inorder_attach(k):
                return True
        elif not self.left_leaf:
            k.parent = self
            self.left_leaf = k
            return True

        # now recur on right child
        if self.right:
            if self.right.inorder_attach(k):
                return True
        elif not self.right_leaf:
            k.parent = self
            self.right_leaf = k
            return True

    def postorder_traversal(self):
        # First recur on left child
        if self.left:
            self.left.postorder_traversal()

        # the recur on right child
        if self.right:
            self.right.postorder_traversal()

        self.postorder_insertion(self)
        j = None
        for i, j in zip(self.higher_dim_tree.leaves_hanging, self.higher_dim_tree.leaves_hanging[1:]):
            if j:
                i.successor = j
                j.predecessor = i
            self.higher_dim_tree.root.inorder_attach(i)
        if j:
            self.higher_dim_tree.root.inorder_attach(j)
        else:
            self.higher_dim_tree.root.inorder_attach(self.higher_dim_tree.leaves_hanging[0])

        if self.dimension is 1:
            self.higher_dim_tree.fill_higher_dim()

    def postorder_insertion(self, node):
        # First recur on left child
        if self.left:
            self.left.postorder_insertion(node)
        else:
            if node.dimension is 1:
                higher_dim_leaf = leaf(self.left_leaf.y, self.left_leaf.x, self.left_leaf.z)
            else:
                higher_dim_leaf = leaf(self.left_leaf.z, self.left_leaf.x, self.left_leaf.y)
            node.higher_dim_tree.leaves_hanging.add(higher_dim_leaf)

        # then recur on right child
        if self.right:
            self.right.postorder_insertion(node)
        elif self.right_leaf:
            if node.dimension is 1:
                higher_dim_leaf = leaf(self.right_leaf.y, self.right_leaf.x, self.right_leaf.z)
            else:
                higher_dim_leaf = leaf(self.right_leaf.z, self.right_leaf.x, self.right_leaf.y)
            node.higher_dim_tree.leaves_hanging.add(higher_dim_leaf)

        # post-order element
        if node.dimension is 1:
            higher_dim_node = AVL_Node(self.y, self.x, self.z, 2)
        else:
            higher_dim_node = AVL_Node(self.z, self.x, self.y, 3)
        node.higher_dim_tree.insert(higher_dim_node)

    def find_split(self, low, high):
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

    def range_query(self, x_low, x_high, y_low, y_high, z_low, z_high):  # limits for each dimension

        x_split = self.find_split(x_low, x_high)
        if x_split is None:
            return

        results = []
        skyline = SortedList()

        x_get_leaves = x_split.left
        while x_get_leaves:
            if x_get_leaves.right:
                y_split = x_get_leaves.higher_dim_tree.root.find_split(y_low, y_high)
                y_split.next_level_query(y_low, y_high, z_low, z_high, results, skyline)

            if x_get_leaves.x <= x_low:
                range_q, dominant = x_get_leaves.higher_dim_tree.root.higher_dim_tree.root.report_leaves(z_low, z_high)
                if range_q:
                    results.extend(range_q)
                    for i in dominant:
                        skyline.add(i)
            x_get_leaves = x_get_leaves.left

        x_get_leaves = x_split.right
        while x_get_leaves:
            if x_get_leaves.x > x_high:
                break
            if x_get_leaves.left:
                y_split = x_get_leaves.higher_dim_tree.root.find_split(y_low, y_high)
                y_split.next_level_query(y_low, y_high, z_low, z_high, results, skyline)
            else:
                range_q, dominant = x_get_leaves.higher_dim_tree.root.higher_dim_tree.root.report_leaves(z_low, z_high)
                if range_q:
                    results.extend(range_q)
                    for i in dominant:
                        skyline.add(i)
            x_get_leaves = x_get_leaves.right

        return results, skyline

    def next_level_query(self, y_low, y_high, z_low, z_high, results, skyline):
        y_get_leaves = self.left
        range_q, dominant = [], []

        while y_get_leaves:
            if y_get_leaves.right:
                range_q, dominant = y_get_leaves.right.higher_dim_tree.root.report_leaves(z_low, z_high)
            if range_q:
                results.extend(range_q)
                for i in dominant:
                    skyline.add(i)
            if y_get_leaves.x <= y_low:
                range_q, dominant = y_get_leaves.higher_dim_tree.root.report_leaves(z_low, z_high)
                if range_q:
                    results.extend(range_q)
                    for i in dominant:
                        skyline.add(i)
            y_get_leaves = y_get_leaves.left

        y_get_leaves = self.right
        while y_get_leaves:
            if y_get_leaves.x > y_high:
                break
            if y_get_leaves.left:
                range_q, dominant = y_get_leaves.left.higher_dim_tree.root.report_leaves(z_low, z_high)
                if range_q:
                    results.extend(range_q)
                    for i in dominant:
                        skyline.add(i)
            else:
                range_q, dominant = y_get_leaves.higher_dim_tree.root.report_leaves(z_low, z_high)
                if range_q:
                    results.extend(range_q)
                    for i in dominant:
                        skyline.add(i)
            y_get_leaves = y_get_leaves.right

    def report_leaves(self, low, high):
        _leaf = self.find_leaf(low)
        if _leaf.x > high:
            return

        results = [_leaf]
        skyline = [_leaf]

        _leaf = _leaf.successor
        while _leaf and _leaf.x <= high:
            results.append(_leaf)
            if _leaf.y <= skyline[-1].y:
                skyline.append(_leaf)
            _leaf = _leaf.successor

        return results, skyline

    def find_leaf(self, k):
        if k > self.x:
            return self.right_leaf or self.right.find_leaf(k)
        else:
            return self.left_leaf or self.left.find_leaf(k)
