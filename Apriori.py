import datetime
import itertools
import argparse
import sys
class apriori:
    def __init__(self,file, support, confidence , printing):
        self.support_value = support
        self.confidence = confidence
        self.filename = file
        self.printing = printing

    def loaddata(self):
        """
        This method is used the load the data from the text file
        :return: it returns a list of sets containing the transaction data
        """
        transactions = []
        with open(self.filename) as f:
            content = [x.strip() for x in f.readlines()]
            for x in content:
                transactions.append(set(x.split(' ')))
        return transactions

    def support_checker(self, unique_items):
        """
        This method is used for checking threshold support value given as a input
        :param unique_items:
        :return: only the items which has more than the threshold value
        """
        accepted = {}
        support = {}
        for key, value in unique_items.items():
            val = value/len(self.transactions)
            if (val >= self.support_value):
                accepted[key] = 1
                support[key] = (val)
        return accepted, support

    def writing(self,subset, leftover,support,coverage,f):
        """
        This is method is used to write only the strong association rule
        :param subset: it is the entire set or union of A and B
        :param leftover: it is set B
        :param support: support value for subset
        :param coverage: coverage value which was calculated for A and B
        :param f: file object to write to the file
        """
        counter = 0
        for i in sorted(list(leftover)):
            if len(leftover) - 1 != counter:
                f.write(i + ", ")
                counter += 1
            else:
                f.write(i)
        f.write(' -> ')
        counter = 0
        for i in sorted(list(subset)):
            if len(subset) - 1 != counter:
                f.write(i + ", ")
                counter += 1
            else:
                f.write(i)
        f.write(" ({0:.2f}".format(support) + ", {})".format(round(coverage,2)))
        f.write("\n")

    def association_rule_generation(self,accepted_list, support_data):
        """
        This method is for caluclating the strong association rule and writing to the file based on user input
        if f is given as an input it will frequent itemset to file
        if a is given as an input it will write frequent itemset and strong association rule
        if r is given as an input it will write strong association rule
        if it is absent then default value x is used and the number of frequent itemsets and number of string association rule is stored in the file
        :param accepted_list: accepted subsets
        :param support_data: it has the support value for all the subset
        """
        total_association_rule = 0
        f = open("apriori_output.txt", "w+")
        if self.printing == "f"or self.printing =="a":
            for i in accepted_list:
                for k in i:
                    counter = 0
                    for i in sorted(k):
                        if len(k) - 1 != counter:
                            f.write(i + ", ")
                            counter += 1
                        else:
                            f.write(str(i) +  " ({0:.2f})".format(support_data[k]) + "\n")
            f.write("\n")

        if self.printing == "x":
            for idx,val in enumerate(accepted_list):
                f.write("Number of frequent {}_itemset"
                        "s: {} \n" .format(idx+1,len(val)))

        if self.printing != "f":
            for i in accepted_list:
                for j in i:
                    if (len(j) > 1):
                        for k in range(len(j)):
                            for subset in itertools.combinations(j, k):
                                left_over = j - set(subset)
                                try:
                                    if k != 0:
                                        coverage = (support_data[j] / support_data[left_over])
                                        if coverage >= self.confidence:
                                            total_association_rule += 1
                                            if self.printing == "r" or self.printing =="a":
                                                self.writing(subset, left_over, support_data[j],coverage,f )
                                except:
                                    print("Exception found")
            if total_association_rule == 0 and self.printing != "x":
                f.write("Number of association rules: {}".format(total_association_rule))
        if self.printing == "x":
            f.write("Number of association rules: {}".format( total_association_rule))
        f.close()


    def generate_candidate(self, accepted_candidate):
        """
        It is used to generate all the possible candidates from the previously accepted candidates
        :param accepted_candidate: previoulsy accepted candidate
        :return: all possible candidate
        """
        accepted = {}
        for key1 in accepted_candidate.keys():
            for key2 in accepted_candidate.keys():
                x = key1 | key2
                if (len(x) == len(key1) + 1) and x not in accepted:
                    accepted[x] = 1
        return accepted
    def subsetchecker(self,item, accepted):
        """
        This is a pruning method here : if A,B,C,D is in item then it is necessary B,C,D ; A,C,D etc should be present. if these
        subsets are not present then its superset is not possible, and we are not checking for A,C ; A,D because if A,C,D is present
        then A,C and A,D will be present
        :param i: item
        :param accepted: previously accepted items
        :return: boolean value whether this itemset is possible or not
        """
        k = len(item) - 1
        for subset in itertools.combinations(item, k):
            if frozenset(subset) not in accepted:
                return False
        return True
    def generate_frequent(self, transaction, candiate,accepted):
        """
        This method calculates the count for the possible candidate and at the same time it prunes the candidate
        it saves a significant amount time since it prevents from checking the transactions and other following contions in it
        :param transaction: transaction data
        :param candiate: all possible candidate
        :param accepted: previously accepted candidates which has more than support value
        :return: total counts for possible candidate while pruning in between
        """
        builder = {}
        # count = 0
        for i in candiate:
            if self.subsetchecker(i,accepted):
                for transac in transaction:
                    # count += 1
                    if i.issubset(transac):
                        if i in builder:
                            builder[i] += 1
                        else:
                            builder[i] = 1
        # print (count)
        return builder


    def generator(self):
        self.transactions = self.loaddata()
        unique_items = {}
        self.first_frequent = True
        for trans in self.transactions:
            for i in trans:
                item = frozenset({i})                                # frequent one itemset is generated
                if item not in unique_items:
                    unique_items[item] = 1
                else:
                    unique_items[item] += 1
        accepted, support = self.support_checker(unique_items)
        accepted_list = [accepted]
        support_data = support
        k = 1
        """
        we will be generating further unique itemset and will be checking their support value, accepted itemset is add to the accepted 
        dictionary and to the support dictionary
        """
        print("Execution for Apriori algorithm started..../")
        # start = datetime.datetime.now()
        while ( len(accepted_list[k-1]) > 0):
            # start = datetime.datetime.now()
            all_candidate = self.generate_candidate( accepted_list[k-1])
            candidate= self.generate_frequent(self.transactions,all_candidate,accepted_list[k-1])
            accepted, support = self.support_checker(candidate)
            accepted_list.append(accepted)
            support_data.update(support)
            k += 1
        # print(start)
        # print((  datetime.datetime.now()) - start)
        self.association_rule_generation(accepted_list,support_data)
        print("Execution completed check apriori_output.txt for ouput ")

def main(sys):
    try :
        file_name = sys.argv[1]
        min_support = float(sys.argv[2])
        min_conf = float(sys.argv[3])
        if (0 <= min_conf <=1) and (0<= min_support <=1):
            try :
                printing = sys.argv[4]
            except:
                printing = "x"
        else:
            raise Exception()
        a = apriori(file_name, min_support, min_conf,printing)
        # a = aprioir('./data100.txt',0.1,.8,"x")
        a.generator()
    except KeyboardInterrupt:
        print('Keyboard Interrupted - Run again to continue')
    except:
        print("Invalid inputs - please the check input")

if __name__ == '__main__':
    main(sys)
