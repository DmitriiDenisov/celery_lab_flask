
from numpy import random
from tqdm import tqdm


def function_gener(N, M):
    whole_list = []
    for i in tqdm(range(N)):
        new_random_list = random.randint(5000, size=M)
        whole_list.append(new_random_list)
    return whole_list


def sum_of_list(whole_list):
    sum_ = 0
    for i in tqdm(range(len(whole_list))):
        for j in range(len(whole_list[i])):
            sum_ += whole_list[i][j]
    return sum_


if __name__ == '__main__':
    whole_list = function_gener(10000, 1500)
    sum_ = sum_of_list(whole_list)




