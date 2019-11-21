# decision-tree
Python implementation and plotting of decision tree algorithms (ID3, C4.5 and CART).

## Requirements
Matplotlib

## Usage
1. Training dataset
First row of which is the attributes, other lines are training samples.

2. Create the decision tree
```
usage: main.py [-h] [--trainset TRAINSET] [--testset TESTSET]

desition tree

optional arguments:
  -h, --help           show this help message and exit
  --trainset TRAINSET  Training dataset filename.
  --testset TESTSET    Testing dataset filename.
``` 

## Reference
 * [Induction of Decision Trees](http://hunch.net/~coms-4771/quinlan.pdf)  
 * [C4.5: programs for machine learning](https://dl.acm.org/citation.cfm?id=152181) 
 * [Classification and regression trees](https://content.taylorfrancis.com/books/download?dac=C2009-0-07054-X&isbn=9781351460491&format=googlePreviewPdf) 