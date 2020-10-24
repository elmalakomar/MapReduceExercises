from random import randint
from pprint import pprint
from functools import reduce
from itertools import groupby
from operator import itemgetter
import matplotlib.pyplot as plt

'''
Given a dataset of songs listened by users,
compute the histogram of songs loved by them
(1 song has been loved by 10 users, 2 songs have been loved by 40 users)
Love means user have listened the song 2+ times.
'''

def dataset_generation(filename = '../data/dataset.txt', user_range = 500, track_range = 500, count_range = 10):
    '''
    Dataset generation for the challenge.
    Can specify how many users, tracks, and the max value for the count.

    Note: generation made with the simple rand list comprehension lead to
    duplicates of userid-trackid
    '''
    ll = []
    for i in range(user_range):
        dd = {}
        dd['User_id'] = f"User{i}"
        for k in range(track_range):
            dd[f"Track{k}"] = randint(0,count_range)
        ll.append(dd)

    with open(filename, "w+") as f:
        f.write(str(ll))
    return ll

def load_dataset(filename = 'dataset.txt'):
    '''
    Load the dataset or generate it if not found.
    '''
    try:
        with open(filename) as f:
            return eval(f.read())
    except FileNotFoundError:
        return dataset_generation(filename = filename)


def aggregate_row(row_dict):
    user = row_dict['User_id']
    row_dict.pop('User_id')
    return [{'userId': user, 'track': key, 'count': value} for key, value in row_dict.items()]


def flat_map(l1, l2):
    return l1+l2

def to_tuple(my_dict):
    return (my_dict['track'],my_dict['count'])

def reduce_by_key1(data, index_key = 0, ) :
    def reducer(tuple1,tuple2):
        return (tuple1[index_key], tuple1[1] + tuple2[1])
    return [reduce(reducer,value) for key, value in groupby(sorted(data), key=itemgetter(index_key))]
'''
Simple example of the value given to the reducer:
    pets = [('dog', 12), ('cat', 15), ('dog', 11), ('cat', 15), ('dog', 10), ('cat', 16)]
    [print(list(group)) for _,group in groupby(sorted(pets), key=itemgetter(0))]
'''

def reduce_by_key2(data, index_key = 0) :
    def reducer(tuple1,tuple2):
        return (tuple1[index_key], tuple1[1] + tuple2[1])
    return [reduce(reducer,value) for key, value in groupby(sorted(data), key=itemgetter(index_key))]

def transform_tuple(data):
    return(data[1],1)


if __name__ == '__main__':
    data = load_dataset()
    #print(data[0]) # [{'User_id': 'User0', 'Track0': 2, 'Track1': 7, ... } {'User_id': 'User1', 'Track0': 2, 'Track1': 7, ... }]
    data = list(map(aggregate_row, data))
    #print(data) # [[{'userId': 'User0', 'track': 'Track0', 'count': 2},{'userId': 'User0', 'track': 'Track1', 'count': 7} ...]]
    data = list(reduce(flat_map, data))
    data = list(map(to_tuple,data))
    # now filter to obtain only loved one
    data = list(filter(lambda x: x[1] > 1,data))

    data = reduce_by_key1(data, index_key = 0)
    data = list(map(transform_tuple,data))
    data = reduce_by_key2(data, index_key=0)
    print(data[0])
    #plot the histogram
    x,y = zip(*data)
    print(x,y)
    plt.bar(x,y)
    plt.show()