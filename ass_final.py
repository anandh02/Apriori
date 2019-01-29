import datetime
import pickle
def preprocessing():
    unique_items = []
    transactions = []
    with open("./data.txt") as f:
        content = [x.strip() for x in f.readlines()]
        for x in content:
            transactions.append(x.split(' '))
            for i in x.split(' '):
                if [i] not in unique_items:
                    unique_items.append([i])
    unique_items.sort()
    return transactions, list(map(frozenset,(unique_items)))

def checker(transactions , unique_item):
    builder = {}
    support_data = {}
    accepted_list = []
    counter = 0
    normalized_value = 1#(1 / len(transactions))
    for transacs in transactions:
        counter +=1
        for item in unique_item:
            if item.issubset(transacs):
                if item in builder:
                    builder[item] += normalized_value
                    if(builder[item] > 10):
                        support_data[item] = builder[item] / len(transactions)
                        if item not in accepted_list :
                            accepted_list.append(item)
                else: builder[item] = normalized_value
    return  support_data,accepted_list
def new_pairs_list(accepted_list,k):
    accepted = []
    for i in range(len(accepted_list)):
        for j in range(i+1 , len(accepted_list)):
            intial_value_1 = sorted(list(accepted_list[i]))[:k-1]
            intial_value_2 = sorted((list(accepted_list[j]))[:k-1])
            if intial_value_1 == intial_value_2 :
                accepted.append(accepted_list[i] | accepted_list[j])
    return accepted
import itertools

def myapriori(accepted_list, support_data):
    min = 0.01
    final_dict = {}
    counter = 0
    for i in accepted_list:
        for j in i :
            if (len(j) > 1):
                for k in range(len(j)-1):
                    for subset in itertools.combinations(j,k) :
                        left_over = j - set(subset)
                        try:
                            if k != 0:
                                coverage =  ( support_data[j] / support_data[left_over])
                                if coverage > 0.8:
                                    final_dict[left_over] = subset
                                else:
                                    print('Yolo')
                        except:
                            counter += 1


    print(final_dict)
    return 0
def combiner():
    transactions, unique_item = preprocessing()
    support_data, accepted_list = checker(transactions , unique_item)
    k=1
    accepted_list = [accepted_list]
    while (len(accepted_list[k-1]) >  0):
        start = datetime.datetime.now()
        accepted = new_pairs_list(accepted_list[k-1],k)
        support, accepted = checker(transactions, accepted)
        accepted_list.append(accepted)
        support_data.update(support)
        k += 1
        print(datetime.datetime.now() - start)
    pickle_out = open("accepted_list.pickle","wb")
    pickle.dump(accepted_list,pickle_out)
    pickle_out = open("support_data.pickle", "wb")
    pickle.dump(support_data, pickle_out)
    pickle_out.close
    myapriori(accepted_list,support_data)

combiner()
def caller():
    pickle_in = open("accepted_list.pickle", "rb")
    accepted_list = pickle.load(pickle_in)
    pickle_in = open("support_data.pickle", "rb")
    support_data = pickle.load(pickle_in)
    myapriori(accepted_list, support_data)

# caller()


def myapriori(accepted_list, support_data):
    for i in accepted_list:
        for j in i :
            print(j)

    return 0