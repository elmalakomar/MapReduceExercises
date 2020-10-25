from random import randint
from functools import reduce
import matplotlib.pyplot as plt
from secrets import randbelow
'''
Use the same dataset to compute:
1. The average number of replays user by user (i.e., how many times in average each user listen songs)
e.g., [User001:12.3, User002:4.2, ...]
2. The Histogram of point (1)
'''

def dataset_generation(filename = 'dataset.txt', user_range = 500, track_range = 500, count_range = 30):
    '''
    Dataset generation for the challenge.
    Can specify how many users, tracks, and the max value for the count.
    Note: generation made with the simple rand list comprehension lead to
    duplicates of userid-trackid
    '''
    ll = []
    for i in range(user_range):
        temp_count_range = randint(5,count_range)
        dd = {}
        dd['User_id'] = f"User{i}"
        for k in range(track_range):
            dd[f"Track{k}"] = randbelow(temp_count_range) + 1 #randint(0,count_range)
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

def expand_row(row):
    user = row['User_id']
    row.pop('User_id')
    return [{'UserId': user, 'count': count} for count in row.values()]

'''
input (row: list of dict): [{'UserId': 'User1', 'count': 0}, {'UserId': 'User1', 'count': 4}, ... ]
output (list of filtered dict): [{'UserId': 'User1', 'count': 4}, ... ]
'''
def map_filter(row_user):
    return [(single_dict['UserId'],single_dict['count']) for single_dict in row_user if single_dict['count'] > 0]

def reducer(tuple1,tuple2):
    return (tuple1[0], tuple1[1] + tuple2[1])

def avg_map(list_of_tuples):
    def avg_reduce(tuple1,tuple2):
        return (tuple1[0],tuple1[1] + tuple2[1])
    size = len(list_of_tuples)
    reduced = reduce(avg_reduce,list_of_tuples)
    return (reduced[0],reduced[1]/size)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    data = load_dataset()
    #print(data[0])
    data = list(map(expand_row,data))
    #print(data[1])
    data = list(map(map_filter, data))
    #print(data[0])
    #data = reduce_by_key(data, index_key=0)
    #data = [reduce(reducer,l)  for l in data]
    data = list(map(avg_map,data))
    print(data)
