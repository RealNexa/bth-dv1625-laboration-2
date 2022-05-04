class AVL:
    class Node:
        def __init__(self):

            self.parent = None
            self.height = 0

            self.left = None
            self.right = None
            self.data = None

    def __init__(self):
        self._root = None
        self.node_id = 0 # ONLY USED WITHIN to_graphviz()!
        pass
    

    def insert(self, element):
        """Inserts a specific element into the BST"""
        new_node = self.Node()
        new_node.data = element

        if self._root is None:
            self._root = new_node
            return

        self.recursive_insert(self._root, new_node)
        self.recursive_hight_calculation(self._root) # can be optimized by only re-calculating the hight one half of the tree?
        self.do_rotations(element, new_node.parent)

    def recursive_insert(self, walker: Node, insertion_node: Node):

        if walker is None: # Base case
            if insertion_node.data < insertion_node.parent.data:
                insertion_node.parent.left = insertion_node

            elif insertion_node.data > insertion_node.parent.data:
                insertion_node.parent.right = insertion_node
            return

        insertion_node.parent = walker

        if insertion_node.data < walker.data:
            self.recursive_insert(walker.left, insertion_node)

        elif insertion_node.data > walker.data:
            self.recursive_insert(walker.right, insertion_node)


    def remove(self, element):
        parent_node = self._recursive_remove(element)
        self.recursive_hight_calculation(self._root) # can be optimized by only re-calculating the hight one half of the tree? 

        if parent_node is not None:
            self.do_rotations(element, parent_node)

    def _recursive_remove(self, element):
        """Removes a specific element from the BST"""
        deletion_node = self.find_node(self._root, element)
        parent_node = None

        if deletion_node is not None:
            
            parent_node = deletion_node.parent

            children_count = self._num_of_children(deletion_node)

            if children_count == 0:
                if deletion_node != self._root:
                    if element < deletion_node.parent.data:
                        deletion_node.parent.left = None
                    elif element > deletion_node.parent.data:
                        deletion_node.parent.right = None

                else:
                    self._root = None


            elif children_count == 1:
                child = deletion_node.left if deletion_node.left is not None else deletion_node.right

                child.parent = deletion_node.parent

                if deletion_node != self._root:
                    if element < deletion_node.parent.data:
                        deletion_node.parent.left = child
                    elif element > deletion_node.parent.data:
                        deletion_node.parent.right = child
                else:
                    self._root = child
                

            elif children_count == 2:
                left_largest = self.get_max_from_node(deletion_node.left)
                parent_node = self.remove(left_largest)
                deletion_node.data = left_largest

        return parent_node



    def do_rotations(self, element, parent_node: Node):
        #TODO HANDLE WHEN ONLY ROOT AND WHEN NO NODES EXIST

        # Parent node is the parrent node of the recently deleted or inserted node
        print(parent_node.data)



    def recursive_hight_calculation(self, node: Node):
        """Calculates and sets each nodes hight"""
        if node is not None:
            node.height = self._recursive_tree_height(node) - 1
            
            self.recursive_hight_calculation(node.left)
            self.recursive_hight_calculation(node.right)


    def find_node(self, node: Node, element):
        
        if node == None:
            return None
        
        elif node.data == element:
            return node

        elif element < node.data:
            return self.find_node(node.left, element)
        
        elif element > node.data:
            return self.find_node(node.right, element)

    def find(self, element):
        result_node = self.find_node(self._root, element)
        
        return True if result_node is not None else False


    def pre_order_walk(self):
        
        num_list = []

        if self._root is not None:
            self._recursive_pre_order(self._root, num_list)
        
        return num_list

    def _recursive_pre_order(self, node: Node, num_list: list):
        
        num_list.append(node.data)                          # Root
        
        if node.left is not None:
            self._recursive_pre_order(node.left, num_list)  # Left
        if node.right is not None:
            self._recursive_pre_order(node.right, num_list) # Right

    def in_order_walk(self):
                
        num_list = []

        if self._root is not None:
            self._recursive_in_order(self._root, num_list)
        
        return num_list

    def _recursive_in_order(self, node: Node, num_list: list):
        
        if node.left is not None:
            self._recursive_in_order(node.left, num_list)   # Left

        num_list.append(node.data)                          # Root

        if node.right is not None:
            self._recursive_in_order(node.right, num_list)  # Right

    def post_order_walk(self):
                
        num_list = []

        if self._root is not None:
            self._recursive_post_order(self._root, num_list)
        
        return num_list

    def _recursive_post_order(self, node: Node, num_list: list):
        
        if node.left is not None:
            self._recursive_post_order(node.left, num_list)     # Left

        if node.right is not None:
            self._recursive_post_order(node.right, num_list)    # Right

        num_list.append(node.data)                              # Root



    def get_tree_height(self):
        """returns amount of children in the gratest path from the root to the end of the BST"""
        if self._root is None:
            return -1
        else:
            return self._recursive_tree_height(self._root) - 1


    def _recursive_tree_height(self, node: Node):
        """recursively gets amount of children in the gratest path from some node to the end of the BST"""
        return max(
                    1 + (self._recursive_tree_height(node.left) if node.left is not None else 0),
                    1 + (self._recursive_tree_height(node.right) if node.right is not None else 0)
                )



    def get_min(self):
        if self._root is not None:
            return self._recursive_get_min(self._root)
        else:
            return -1

    def _recursive_get_min(self, node: Node):
        
        # Base case
        if node.left is None:
            return node.data

        else:
            return self._recursive_get_min(node.left) 


    def get_max(self):
        if self._root is not None:
            return self._recursive_get_max(self._root)
        else:
            return -1

    def _recursive_get_max(self, node: Node):
        # Base case
        if node.right is None:
            return node.data

        else:
            return self._recursive_get_max(node.right) 


    def _num_of_children(self, node):
        """returns number of children the inputed node has"""
        counter = 0
        if node.left is not None:
            counter += 1
        if node.right is not None:
            counter += 1
        return counter



    def get_max_from_node(self, node: Node):
        """Returns the largest number after a specific node"""
        largest = node.data
        while node.right is not None:
            node = node.right
            largest = node.data

        return largest


    def to_graphviz_rec(self, data, current: Node):
        my_node_id = self.node_id
        data += "\t" + str(my_node_id) + " [label=\"" + str(current.height) + "\\n" + str(current.data) + "\"];\n" ;
        self.node_id += 1
        if current.left is not None:
            data += "\t" +  str(my_node_id) + " -> " + str(self.node_id) + " [color=blue];\n";
            data = self.to_graphviz_rec(data, current.left)
        else:
            data += "\t" + str(self.node_id) + " [label=nill,style=invis];\n";
            data += "\t" +  str(my_node_id) + " -> " + str(self.node_id) + " [style=invis];\n";

        self.node_id += 1
        if current.right is not None:
            data += "\t" +  str(my_node_id) + " -> " + str(self.node_id) + " [color=red];\n";
            data = self.to_graphviz_rec(data, current.right);
        else:
            data += "\t" + str(self.node_id) + " [label=nill,style=invis];\n";
            data += "\t" +  str(my_node_id) + " -> " + str(self.node_id) + " [style=invis];\n";
        
        return data
    
    def to_graphviz(self):
        data = ""
        if self._root is not None:
            self.node_id = 0
            data += "digraph {\n"
            data += "\tRoot [shape=plaintext];\n"
            data += "\t\"Root\" -> 0 [color=black];\n"
            data = self.to_graphviz_rec(data, self._root)
            data += "}\n"
        return data


def main():
    avl = AVL()
    avl.insert(15)
    avl.insert(13)
    avl.insert(20)
    avl.insert(9)
    avl.insert(14)
    avl.insert(19)
    avl.insert(55)
    avl.insert(8)
    avl.insert(10)
    avl.insert(45)
    avl.insert(7)
    avl.remove(7)
    # print("Found 45: {}".format(bst.find(45)))
    # print("Found 15: {}".format(bst.find(15)))
    # print("Found 10: {}".format(bst.find(10)))
    # print("Found 8: {}".format(bst.find(8)))
    # print("Found 14: {}".format(bst.find(14)))
    # print("Found 20: {}".format(bst.find(20)))
    # print("Found 55: {}".format(bst.find(55)))
    # print("Found 100: {}".format(bst.find(100)))
    # print("Tree hight: {}".format(bst.get_tree_height()))
    # print("Pre order walk: {}".format(bst.pre_order_walk()))
    # print("In order walk: {}".format(bst.in_order_walk()))
    # print("Post order walk: {}".format(bst.post_order_walk()))
    # print("Min: {}".format(bst.get_min()))
    # print("Max: {}".format(bst.get_max()))

    # bst.remove(55)
    # bst.remove(20)
    # bst.remove(13)
    # bst.remove(15)
    # bst.remove(14)
    # bst.remove(10)
    # bst.remove(9)
    # bst.remove(8)
    # bst.remove(19)
    # bst.remove(45)

    # print("\nEmpty:")
    # print("Tree hight: {}".format(bst.get_tree_height()))
    # print("Pre order walk: {}".format(bst.pre_order_walk()))
    # print("In order walk: {}".format(bst.in_order_walk()))
    # print("Post order walk: {}".format(bst.post_order_walk()))
    # print("Min: {}".format(bst.get_min()))
    # print("Max: {}".format(bst.get_max()))

    # bst.insert(100)
    # bst.insert(25)
    # bst.insert(25)
    # bst.insert(25)
    # bst.insert(500)
    # bst.insert(500)
    # bst.insert(500)
    # bst.insert(500)
    # bst.insert(501)
    # bst.insert(500)

    # print("Pre order walk: {}".format(bst.pre_order_walk()))
    # print("In order walk: {}".format(bst.in_order_walk()))
    # print("Post order walk: {}".format(bst.post_order_walk()))
    print(avl.to_graphviz())

if __name__ == '__main__':
    main()