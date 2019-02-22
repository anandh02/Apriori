import itertools
import argparse
class aprioir:
    def __init__(self,file, support, confidence, printing):
        self.support_value = support
        self.confidence = confidence
        self.filename = file
        self.printing = printing

    def loaddata(self):
        transactions = []
        unique_items = []
        with open(self.filename) as f:
            content = [x.strip() for x in f.readlines()]
            for x in content:
                transactions.append(x.split(' '))
        return transactions

    def support_checker(self, unique_items):
        accepted = []
        support = {}
        for key, value in unique_items.items():
            val = value/len(self.transactions)
            if (val >= self.support_value):
                accepted.append(key)
                support[key] = (val)
        return accepted, support

    def writing(self,j, leftover,support,coverage,f):
        counter = 0
        for i in sorted(leftover):
            if len(leftover) - 1 != counter:
                f.write(i + ", ")
                counter += 1
            else:
                f.write(i)
        f.write(' -> ')
        counter = 0
        for i in sorted(j):
            if len(j) - 1 != counter:
                f.write(i + ", ")
                counter += 1
            else:
                f.write(i)
        f.write(" ({0:.2f}".format(support) + ", {})".format(coverage))
        f.write("\n")

    def myapriori(self,accepted_list, support_data):
        final_dict = {}
        f = open("Aprioi_output.txt", "w+")

        if self.printing == "f"or self.printing =="a":
            f.write("Frequent Item set \n")
            for i in accepted_list:
                x = len(i)
                # i = list(i)
                # counter = 0
                for k in i:
                    counter = 0
                    for i in sorted(k):
                        if len(k) - 1 != counter:
                            f.write(i + ", ")
                            counter += 1
                        else:
                            # f.write(i)
                        # if (x - 1) != 0:
                            f.write(str(i) +  " ({0:.2f})".format(support_data[k]) + "\n")
                            # x -= 1
                        # else:
                        #     f.write(str((j)) +" {0:.2f}".format(support_data[k]) + "\n")
            f.write("\n")

        if self.printing == "x":
            for idx,val in enumerate(accepted_list):
                f.write("Number of frequent {}_itemset"
                        "s: {} \n" .format(idx+1,len(val)))

        if self.printing != "f":
            if self.printing == "r" or self.printing == "a":
                f.write("Strong Association rule \n")
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
                                            final_dict[left_over] = subset
                                            if self.printing == "r" or self.printing =="a":
                                                self.writing(subset, left_over, support_data[j],coverage,f )
                                except:
                                    print("Exception found")
        if self.printing == "x":
            f.write("Number of association rules: {}".format( len(final_dict) ) )
        f.close()


    def generate_candidate(self, support,k):
        accepted = []
        for i in range(len(support)):
            for j in range(i+1,len(support)):
                intial_value_1 = sorted(list(support[i]))[:k - 1]
                intial_value_2 = sorted(list(support[j]))[:k - 1]
                if intial_value_1 == intial_value_2:
                    accepted.append(support[i] | support[j])
        return accepted
    def generate_frequent(self, transaction, candiate):
        builder = {}
        count = 0
        for transac in transaction:
            count += 1
            for i in candiate:
                if i.issubset(transac):
                    if i in builder:
                        builder[i] += 1
                    else:
                        builder[i] = 1
        return builder


    def generator(self):
        self.transactions = self.loaddata()
        unique_items = {}
        accepted_list = []
        support_data = {}
        self.first_frequent = True
        for trans in self.transactions:
            for i in trans:
                item = frozenset({i})
                if item not in unique_items:
                    unique_items[item] = 1      #self.normalized_value
                else:
                    unique_items[item] += 1     #self.
        accepted, support = self.support_checker(unique_items)
        accepted_list = [accepted]
        support_data = support
        k = 1
        while ( len(accepted_list[k-1]) > 0):
            all_candidate = self.generate_candidate( accepted_list[k-1],k)
            candidate= self.generate_frequent(self.transactions,all_candidate)
            accepted, support = self.support_checker(candidate)
            accepted_list.append(accepted)
            support_data.update(support)
            k += 1
        print(accepted_list)
        self.myapriori(accepted_list,support_data)

def main():
    myparser = argparse.ArgumentParser(description='Apriori Algorithm')
    myparser.add_argument("file_name", help="file name")
    myparser.add_argument("min_support", help="min support")
    myparser.add_argument("min_conf", help="min confidence")
    myparser.add_argument("printing", default= 'x',help="printing format")

    args = myparser.parse_args()

    a =  aprioir(args.file_name, float(args.min_support), float(args.min_conf), args.printing)
    # a = aprioir('./testdata.txt',0.22,0.7,"r")
    a.generator()

if __name__ == '__main__':
    main()
