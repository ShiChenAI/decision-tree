import operator

def read_file(file_name, mode='trainset'):
    with open(file_name, 'r') as f:
        dataset = []
        classes = []
        for i, line in enumerate(f.readlines()):
            line = line.strip().split(',')
            if mode == 'trainset' and i == 0:
                # classes
                classes = [l for l in line]
            else:
                dataset.append(line)

    return dataset, classes


def get_subset(dataset, axis, value):
    sub_dataset = []
    for sample in dataset:
        if sample[axis] == value:
            reduced_sample = sample[:axis] 
            reduced_sample.extend(sample[axis+1: ])
            sub_dataset.append(reduced_sample)

    return sub_dataset


def majority_count(class_list):
    class_count = {}
    for vote in class_list:
        if vote not in class_count.keys():
            class_count[vote] = 0
        class_count[vote] += 1
    sorted_class_cont = sorted(class_count.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_class_cont[0][0]
