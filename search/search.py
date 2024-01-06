
class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class Tree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        if self.root is None:
            self.root = Node(data)
        else:
            self._insert_recursive(self.root, data)

    def _insert_recursive(self, node, data):
        if data < node.data:
            if node.left is None:
                node.left = Node(data)
            else:
                self._insert_recursive(node.left, data)
        else:
            if node.right is None:
                node.right = Node(data)
            else:
                self._insert_recursive(node.right, data)

    def traverse(self, order):
        result = []
        if order == 'pre':
            self._preorder_traversal_recursive(self.root, result)
        elif order == 'in':
            self._inorder_traversal_recursive(self.root, result)
        elif order == 'post':
            self._postorder_traversal_recursive(self.root, result)
        return result

    def _preorder_traversal_recursive(self, node, result):
        if node:
            result.append(node.data)
            self._preorder_traversal_recursive(node.left, result)
            self._preorder_traversal_recursive(node.right, result)

    def _inorder_traversal_recursive(self, node, result):
        if node:
            self._inorder_traversal_recursive(node.left, result)
            result.append(node.data)
            self._inorder_traversal_recursive(node.right, result)

    def _postorder_traversal_recursive(self, node, result):
        if node:
            self._postorder_traversal_recursive(node.left, result)
            self._postorder_traversal_recursive(node.right, result)
            result.append(node.data)



lst0 = [8, 3, 10, 1, 6, 14, 4, 7, 13]
tree = Tree()
for data in lst0:
    tree.insert(data)


print(tree.traverse('pre'))

