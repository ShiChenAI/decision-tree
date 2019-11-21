import matplotlib.pyplot as plt
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['Noto Sans CJK JP']

class TreePlotter:
    """Tree architecture plotter.
    """    
    
    def __init__(self, tree, name):
        self.tree = tree
        self.name = name
        self.axes = None
        self.total_w = 0
        self.total_d = 0
        self.x_off = 0
        self.y_off = 0


    def _get_num_leaves(self, tree):
        """Get the number of leaves.
        
        Arguments:
            tree {dictionary} -- Trained tree.
        
        Returns:
            integrt -- Number of leaves.
        """        

        num_leafs = 0
        root_node_name = list(tree.keys())[0]
        children_nodes = tree[root_node_name]
        for key in children_nodes.keys():
            if type(children_nodes[key]).__name__ == 'dict':
                num_leafs += self._get_num_leaves(children_nodes[key])
            else:
                num_leafs += 1
        return num_leafs


    def _get_tree_depth(self, tree):
        """Get max depth of the tree.
        
        Arguments:
            tree {dictionary} -- Trained tree.
        
        Returns:
            integer -- Max depth of the tree.
        """        

        max_depth = 0
        root_node_name = list(tree.keys())[0]
        children_nodes = tree[root_node_name]
        for key in children_nodes.keys():
            if type(children_nodes[key]).__name__ == 'dict':
                cur_depth = self._get_tree_depth(children_nodes[key]) + 1
            else:
                cur_depth = 1
            if cur_depth > max_depth:
                max_depth = cur_depth
        return max_depth


    def _plot_mid_text(self, center_pt, parent_pt, txt_string):
        """Plot middle text between nodes.
        
        Arguments:
            center_pt {list} -- Center point of node.
            parent_pt {list} -- Point of the parent.
            txt_string {string} -- Text string.
        """        

        x_mid = (parent_pt[0] - center_pt[0]) / 2.0 + center_pt[0]
        y_mid = (parent_pt[1] - center_pt[1]) / 2.0 + center_pt[1]
        self.axes.text(x_mid, y_mid, txt_string)


    def _plot_node(self, node_txt, center_pt, parent_pt, node_type):
        """Plot the node.
        
        Arguments:
            node_txt {string} -- Node text.
            center_pt {string} -- Center point of the node.
            parent_pt {[type]} -- Point of the parent.
            node_type {dictionary} -- Node type.
        """        
        self.axes.annotate(node_txt, xy=parent_pt, xycoords='axes fraction',
                           xytext=center_pt, textcoords='axes fraction',
                           va='center', ha='center', bbox=node_type, arrowprops=dict(arrowstyle='<-'))


    def _plot_tree(self, tree, parent_pt, node_txt):
        """Plot the tree.
        
        Arguments:
            tree {dictionary} -- Trained tree.
            parent_pt {[type]} -- Point of the parent.
            node_txt {string} -- Node text.
        """        

        num_leafs = self._get_num_leaves(tree)
        root_node_name = list(tree.keys())[0]
        center_pt = (self.x_off + (1.0 + float(num_leafs)) / 2.0 / self.total_w, self.y_off)
        self._plot_mid_text(center_pt, parent_pt, node_txt)
        self._plot_node(root_node_name, center_pt, parent_pt, dict(boxstyle='sawtooth', fc='0.8'))
        children_nodes = tree[root_node_name]
        self.y_off = self.y_off - 1.0 / self.total_d
        for node_name in children_nodes.keys():
            if type(children_nodes[node_name]).__name__ == 'dict':
                self._plot_tree(children_nodes[node_name], center_pt, str(node_name))
            else:
                self.x_off  = self.x_off  + 1.0 / self.total_w
                self._plot_node(children_nodes[node_name], (self.x_off , self.y_off), center_pt, dict(boxstyle='round4', fc='0.8'))
                self._plot_mid_text((self.x_off , self.y_off), center_pt, str(node_name))

        self.y_off = self.y_off + 1.0 / self.total_d


    def plot(self):
        """Plot graph.
        """        

        fig = plt.figure(2, facecolor='white')
        fig.clf()
        axprops = dict(xticks=[], yticks=[])
        self.axes = plt.subplot(111, frameon=False, **axprops)
        self.total_w = float(self._get_num_leaves(self.tree))
        self.total_d = float(self._get_tree_depth(self.tree))
        self.x_off = -0.5 / self.total_w
        self.y_off= 1.0
        self._plot_tree(self.tree , (0.5, 1.0), '')
        plt.title(self.name, fontsize=12, color='red')
        plt.show()