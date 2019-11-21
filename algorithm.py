from math import log
from utils import get_subset, majority_count

class Tree:
    """Calculate the tree architecture.
    """    
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes


    def _compute_entropy(self, dataset):
        """Compute entropy.
        
        Arguments:
            dataset {list} -- Training dataset.
        
        Returns:
            float -- Calculated entropy.
        """

        n_samples = len(dataset)
        n_labels = {}
        
        for sample in dataset:
            cur_label = sample[-1]
            if cur_label not in n_labels.keys():
                n_labels[cur_label] = 0
            n_labels[cur_label] += 1
        
        ent = 0.0
        for n_label in n_labels.values():
            p = float(n_label) / n_samples
            ent = ent - p*log(p, 2)
        
        return ent


    def _select_attribute(self, dataset):
        """Select attribute to split subset.
        
        Arguments:
            dataset {list} -- Training dataset.
        
        Returns:
            integer -- Selected attribute index.
        """        

        n_features = len(dataset[0]) - 1
        base_entropy = self._compute_entropy(dataset)
        if self.name == 'ID3':
            max_info_gain = 0.0
        elif self.name == 'C45':
            max_info_gain_ratio = 0.0
        elif self.name == 'CART':
            min_gini = 99999.0

        selected_attribute = -1
        for i in range(n_features):
            attribute_list = [sample[i] for sample in dataset]  
            unique_vals = set(attribute_list)
            sub_entropy = 0.0
            if self.name == 'C45':
                iv = 0.0
            elif self.name == 'CART':
                gini = 0.0
            for val in unique_vals:
                sub_dataset = get_subset(dataset, i, val)
                p = len(sub_dataset) / float(len(dataset))
                if self.name == 'CART':
                    sub_p = len(get_subset(sub_dataset, -1, '0')) / float(len(sub_dataset))
                else:
                    sub_entropy += p * self._compute_entropy(sub_dataset)
                if self.name == 'C45':
                    iv = iv - p * log(p, 2)
                elif self.name == 'CART':
                    gini += p * (1.0 - pow(sub_p, 2) - pow(1 - sub_p, 2))
                    print('{0:d}th information gini in CART is：{1:.3f}'.format(i, gini))

            info_gain = base_entropy - sub_entropy
            if self.name == 'ID3':
                print('{0:d}th information gain in ID3 is：{1:3f}'.format(i, info_gain))
                if info_gain > max_info_gain:
                    max_info_gain = info_gain
                    selected_attribute = i
            elif self.name == 'C45':
                if iv == 0:
                    continue
                info_gain_ratio = info_gain / iv
                print('{0:d}th information gain rario in C4.5 is：{1:3f}'.format(i, info_gain_ratio))
                if info_gain_ratio > max_info_gain_ratio:
                    max_info_gain_ratio = info_gain_ratio
                    selected_attribute = i
            elif self.name == 'CART':
                if gini < min_gini:
                    min_gini = gini
                    selected_attribute = i

        return selected_attribute


    def _make_desicion(self, tree, sample):
        """Make decision using the trained tree.
        
        Arguments:
            tree {dictionary} -- Trained tree.
            sample {list} -- Sample for decision making.
        
        Returns:
            string -- Decision.
        """        

        root_node_name = list(tree.keys())[0]
        children_nodes = tree[root_node_name]
        attribute_index = self.attributes.index(root_node_name)
        desicion = '0'
        for key in children_nodes.keys():
            if sample[attribute_index] == key:
                if type(children_nodes[key]).__name__ == 'dict':
                    desicion = self._make_desicion(children_nodes[key], sample)
                else:
                    desicion = children_nodes[key]

        return desicion


    def create_tree(self, dataset, attributes):
        """Create decision tree using trainset.
        
        Arguments:
            dataset {list} -- Training dataset.
            attributes {list} -- Attributes.
        
        Returns:
            dictionary -- Trained decision tree.
        """        

        class_list = [sample[-1] for sample in dataset]
        if class_list.count(class_list[0]) == len(class_list):
            return class_list[0]
        if len(dataset[0]) == 1:
            return majority_count(class_list)

        selected_attribute = self._select_attribute(dataset)
        selected_attribute_label = attributes[selected_attribute]
        print('Current selected attribute: ', selected_attribute_label)
        tree = {selected_attribute_label: {}}
        del(attributes[selected_attribute])

        attribute_list = [sample[selected_attribute] for sample in dataset] 
        unique_vals = set(attribute_list)
        for val in unique_vals:
            sub_attributes = attributes[:]
            tree[selected_attribute_label][val] = self.create_tree(get_subset(dataset, selected_attribute, val), sub_attributes)

        return tree    


    def test(self, tree, testset):
        """Test.
        
        Arguments:
            tree {sictionary} -- Trained tree.
            testset {list} -- Testset.
        
        Returns:
            lsit -- Decisions.
        """        

        desicions = []
        for sample in testset:
            desicions.append(self._make_desicion(tree, sample))
        return desicions
