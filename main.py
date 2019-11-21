from utils import read_file
from algorithm import Tree
from plotter import TreePlotter
import argparse

def get_args():
    parser = argparse.ArgumentParser(description='desition tree')
    parser.add_argument('--trainset', type=str, default='dataset.txt',
                        help='Training dataset filename.')
    parser.add_argument('--testset', type=str, default='testset.txt',
                        help='Testing dataset filename.')
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    trainset, attributes = read_file(args.trainset, 'trainset')
    print('attributes:\n', attributes)
    print('dataset:\n', trainset)
    print('---------------------------------------------')
    
    while(True):    
        str_input = str(input('Selet algorithm:->(1:ID3; 2:C4.5; 3:CART)|(enter q to quit!)|：'))
        if str_input == '1':
            alg_name = 'ID3'
        elif str_input == '2':
            alg_name = 'C45'
        elif str_input == '3':
            alg_name = 'CART'
        elif str_input == 'q':
            break
        
        print('----------------Creating tree----------------')
        tr = Tree(alg_name, attributes)
        attributes_tmp = attributes[:]
        tree = tr.create_tree(trainset, attributes_tmp)
        print('tree:\n', tree)
        tp = TreePlotter(tree, alg_name)
        tp.plot()

        testset, _ = read_file(args.testset, 'testset')
        print('---------------------------------------------')
        print('Testing results：\n')
        print(tr.test(tree, testset))