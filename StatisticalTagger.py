# coding: utf-8
# author :jayarama kapil sridhara

import re
from nltk.data import load
from collections import defaultdict
from collections import Counter
tagdict = load('help/tagsets/upenn_tagset.pickle')
tag_list = tagdict.keys()

def CleanFile():
    """
    This function is used to clean the Input Brown snapshot file
    """
    global final_list
    with open('SnapshotBROWN.pos.all.txt' , 'r+') as f:
        data = f.readlines()
        mylist = []  
        other_list = []                                                               
        for lines in data:                                                                                                       
            if lines == '     (. .))\n':
                mylist.append(other_list)
                other_list = []
            else:

        out_list = []
        pre_final_list=[]
        for i in mylist:
            p =re.findall("[^-()\n.`':,$ ]+",(' '.join(i)))
            q = []
            for j in range(0,len(p)):
                if p[j] in tag_list:
                    q.extend([p[j],p[j+1]])
            pre_final_list.append(q)
        file = open('BROWN-clean.pos.txt', 'w')
        for i in pre_final_list:
            file.write(' '.join(i))
            file.write('\n')
        file.close()
        final_list = [item for sublist in pre_final_list for item in sublist]

        
def HashOfHash(): 
    """
    This function is used for Hashing of words and thier tags which looks as follows : {'word':{'tag1':count,'tag2':count}} 
    """
    global hash_dict
    with open('BROWN-clean.pos.txt', 'r+') as f:
        data = f.read()
        data = data.split()
        word_dict= defaultdict(lambda: [])
        for i in range(0,len(data)-1):
            if data[i]  in tag_list:
                word_dict[data[i+1]].append(data[i])
        hash_dict = {k: dict(Counter(v)) for k, v in word_dict.items()}
        return ('Hash of Hashes of words and tags is given by: {} '.format(hash_dict))


def FrequentTags():
    """
    This functions returns top 20 frequent tags
    """
    global top_list
    HashOfHash()
    frequent_tags = defaultdict(int)
    for dicts in hash_dict.values():
        for i, j in dicts.items():
            frequent_tags[i] += j
    top_list= sorted(frequent_tags.items(), key=lambda kv: kv[1], reverse=True)
    
    return ('The top 20 Tags and their counts are given by: {}'.format(top_list[:20]))


def EvaluateTagger():
    """
    This function is used to calculate the accuaracy after assigning the most frequent tag to all words.
    """
    CleanFile()
    FrequentTags()
    MostFrequent_tag = top_list[0][0]
    Evaluated_list = final_list
    Original_tags=[]
    Evaluated_tags =[]
    for i in range(0,len(Evaluated_list)):
        if Evaluated_list[i] in tag_list:
            Original_tags.append(Evaluated_list[i])
            Evaluated_tags.append(MostFrequent_tag)
            Evaluated_list[i]=MostFrequent_tag     
    count = 0
    for i in range(0,len(Evaluated_tags)):
        if Evaluated_tags[i]==Original_tags[i]:
            count = count+1
    accuracy = (count/len(Evaluated_tags))*100
    return('The accuracy of the tagger is {}'.format(accuracy))


def main():
    """
    main function which runs all the above defined functions
    """
    CleanFile()
    print(HashOfHash())
    print('\n')
    print(FrequentTags())
    print('\n')
    print(EvaluateTagger())

main()
