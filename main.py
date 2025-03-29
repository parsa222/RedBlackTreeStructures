import random
from itertools import permutations
from flask import Flask, render_template_string
import math





#go to the end of this file to change the variables

class RBNode:
    def __init__(self, value, color='red'):
        self.value = value
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

    def grandparent(self):
        if self.parent is None:
            return None
        return self.parent.parent

    def sibling(self):
        if self.parent is None:
            return None
        if self == self.parent.left:
            return self.parent.right
        return self.parent.left

    def uncle(self):
        if self.parent is None:
            return None
        return self.parent.sibling()

class RedBlackTree:
    #copied RB tree class from geeks4geeks
    def __init__(self):
        self.root = None

    def insert(self, value):
        new_node = RBNode(value)
        if self.root is None:
            self.root = new_node
        else:
            curr_node = self.root
            while True:
                if value < curr_node.value:
                    if curr_node.left is None:
                        curr_node.left = new_node
                        new_node.parent = curr_node
                        break
                    else:
                        curr_node = curr_node.left
                else:
                    if curr_node.right is None:
                        curr_node.right = new_node
                        new_node.parent = curr_node
                        break
                    else:
                        curr_node = curr_node.right
        self.insert_fix(new_node)

    def insert_fix(self, new_node):
        while new_node.parent and new_node.parent.color == 'red':
            if new_node.parent == new_node.grandparent().left:
                uncle = new_node.uncle()
                if uncle and uncle.color == 'red':
                    new_node.parent.color = 'black'
                    uncle.color = 'black'
                    new_node.grandparent().color = 'red'
                    new_node = new_node.grandparent()
                else:
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self.rotate_left(new_node)
                    new_node.parent.color = 'black'
                    new_node.grandparent().color = 'red'
                    self.rotate_right(new_node.grandparent())
            else:
                uncle = new_node.uncle()
                if uncle and uncle.color == 'red':
                    new_node.parent.color = 'black'
                    uncle.color = 'black'
                    new_node.grandparent().color = 'red'
                    new_node = new_node.grandparent()
                else:
                    if new_node == new_node.parent.left:
                        new_node = new_node.parent
                        self.rotate_right(new_node)
                    new_node.parent.color = 'black'
                    new_node.grandparent().color = 'red'
                    self.rotate_left(new_node.grandparent())
        self.root.color = 'black'

    def rotate_left(self, node):
        right_child = node.right
        node.right = right_child.left
        if right_child.left is not None:
            right_child.left.parent = node
        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child
        right_child.left = node
        node.parent = right_child

    def rotate_right(self, node):
        left_child = node.left
        node.left = left_child.right
        if left_child.right is not None:
            left_child.right.parent = node
        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child
        left_child.right = node
        node.parent = left_child

    def to_html(self, node=None):
        if node is None:
            node = self.root
        if node is None:
            return "<div style='margin:10px;'>Empty Tree</div>"
        color = 'red' if node.color == 'red' else 'black'
        left_html = self.to_html(node.left) if node.left else "<div style='border:1px solid gray; padding:5px; margin:5px; color:gray;'>NIL</div>"
        right_html = self.to_html(node.right) if node.right else "<div style='border:1px solid gray; padding:5px; margin:5px; color:gray;'>NIL</div>"
        return f"""
        <div style='display:inline-block; text-align:center; margin:10px;'>
            <div style='display:inline-block; border:2px solid {color}; border-radius:50%; width:40px; height:40px; line-height:40px; color:{color};'>
                {node.value}
            </div>
            <div style='display:flex; justify-content:space-around;'>
                {left_html}
                {right_html}
            </div>
        </div>
        """

    def encode_structure(self):
        """
        encoding each tree to know that structure already exists
        left = L
        right = R
        Root = T
        black = B
        red = D


        """
        codes = []
        def dfs(node, path):
            if node is None:
                return
            color_code = 'B' if node.color == 'black' else 'D'
            node_code = path + color_code
            codes.append(node_code)
            dfs(node.left, path + 'L')
            dfs(node.right, path + 'R')

        if self.root is None:
            return "EMPTY"
        dfs(self.root, 't')
        codes.sort()
        return ''.join(codes)

    def color_all_black(self):
        def color_black(node):
            if node:
                node.color = 'black'
                color_black(node.left)
                color_black(node.right)
        color_black(self.root)


def is_perfect_number(n):
    # check if n = 2^k - 1 
    return (n+1 & n) == 0  #  n+1 is power of 2 if (n+1 & n) == 0 OPERAND



# if n=7 or 3 it means that all black tree is also possible because you can remove one red node at the end 
def build_perfect_all_black_tree(n):

   
    def build_balanced(keys):
        if not keys:
            return None
        mid = len(keys)//2
        node = RBNode(keys[mid], color='black')
        left_sub = build_balanced(keys[:mid])
        right_sub = build_balanced(keys[mid+1:])
        node.left = left_sub
        if left_sub:
            left_sub.parent = node
        node.right = right_sub
        if right_sub:
            right_sub.parent = node
        return node

    tree = RedBlackTree()
    keys = list(range(1, n+1))
    tree.root = build_balanced(keys)
    # all black already
    return tree


app = Flask(__name__)

@app.route('/')
def show_structures():
    global NumberOfNodes
    NUM_TRIALS = 2   
    N = NumberOfNodes         # change here ,update = nevermind do not TOUCH :D
    all_structures = set()
    structures_info = []

    for trial_i in range(1, NUM_TRIALS+1):
        keys = random.sample(range(1, 100), N)
        for perm in permutations(keys):
            tree = RedBlackTree()
            for v in perm:
                tree.insert(v)
            encoded = tree.encode_structure()
            if encoded not in all_structures:
                all_structures.add(encoded)
                structures_info.append((encoded, tree.to_html(), perm))

    # If n makes a perefect number
    if is_perfect_number(N):
        perfect_black_tree = build_perfect_all_black_tree(N)
        encoded = perfect_black_tree.encode_structure()
        if encoded not in all_structures:
            all_structures.add(encoded)
            # there's no insertion order here, we can just say none or [] 
            structures_info.append((encoded, perfect_black_tree.to_html(), ["Constructed Perfect Tree"]))

    html_list = []
    html_list.append(f"<h1>all distinct structures for {NumberOfNodes} nodes</h1>")
    html_list.append(f"<p>total distinct structures: {len(all_structures)}</p>")

    idx = 1
    for encoded, html_tree, order in structures_info:
        order_str = ", ".join(map(str, order))
        html_list.append(f"<h3>structure {idx}</h3><p>encoded: {encoded}<br>insertion order: {order_str}</p>{html_tree}")
        idx += 1

    html_content = f"""
    <html>
    <head><title>distinct RB Structures</title></head>
    <body>
    <h1>permutation of keys for each trial</h1>
    {''.join(html_list)}
    </body>
    </html>
    """
    return render_template_string(html_content)




#change this 
NumberOfNodes = 7
#default port on flask is 5000 but i was running sth else on 5000 so i used 8080 
app.run(debug=True,port=8080)
