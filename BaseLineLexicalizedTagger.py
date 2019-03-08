# coding: utf-8
# author :jayarama kapil sridhara

# 're' is the regular expression package for python, we need to import this package to parse the input file
import re

# Please import NLTK package since I am using this package to identify the POS (parts of speech) tags in the input file 
from nltk.data import load

# Default dictionary provided from collections module for hasing etc..
from collections import defaultdict

# Counter funciton is imported to count the number of items of a list or dictionary 
from collections import Counter

# Loading the University of Pennsylvania tagset
tagdict = load('help/tagsets/upenn_tagset.pickle')

# forming a list of tags
tag_list = tagdict.keys()

# The tag list looks as below:

#dict_keys(['LS', 'TO', 'VBN', "''", 'WP', 'UH', 'VBG', 'JJ', 'VBZ', '--', 'VBP', 'NN', 'DT', 'PRP', ':', 'WP$', 'NNPS', 'PRP$', 'WDT', '(', ')', '.', ',', '``', '$', 'RB', 'RBR', 'RBS', 'VBD', 'IN', 'FW', 'RP', 'JJR', 'JJS', 'PDT', 'MD', 'VB', 'WRB', 'NNP', 'EX', 'NNS', 'SYM', 'CC', 'CD', 'POS'])


def CleanFile():
    
    """
    This function is used to clean the Input Brown snapshot file
    
    """
    # The final list is declared as a global variable which consists of list of words and tags. It is declared Global since it will be accessed outside fo this function 
    global final_list
    
    # The below code segment converts the input file and forms chunks of sentence lists in mylist
    
    with open('SnapshotBROWN.pos.all.txt' , 'r+') as f:
        data = f.readlines()
        mylist = []  
        other_list = []                                                               
        for lines in data:                                                                                                       
            if lines == '     (. .))\n':
                mylist.append(other_list)
                other_list = []
            else:
                other_list.append(lines)
    #
    # The below code segement parses the input brown file and removes these literals: [^-()\n.`':,$ ]+ from the input file and forms a pre final list which contains cleaned list of each sentence of the brown file
        out_list = []
        pre_final_list=[]
        for i in mylist:
            p =re.findall("[^-()\n.`':,$ ]+",(' '.join(i)))
            q = []
            for j in range(0,len(p)):
                if p[j] in tag_list:
                    q.extend([p[j],p[j+1]])
            pre_final_list.append(q)
    #
    # The below code segment is to write sentences to the brown clean file 
        file = open('BROWN-clean.pos.txt', 'w')
        for i in pre_final_list:
            file.write(' '.join(i))
            file.write('\n')
        file.close()
        
    #
    # final list is the global variable which is declared above it consists  of all the tokens of words and tags which is used in Evaluate  function calculating the accuracy
        final_list = [item for sublist in pre_final_list for item in sublist]

        
def HashOfHash():
    
    """
    This function is used for Hashing of words and thier tags which looks as follows : {'word':{'tag1':count,'tag2':count}}
    
    """
    global hash_dict
    
    # The below code segment hashes words and tags to their counts using default dictionary 
    # The output of this function looks as follows
    # {'The': {'DT': 24}, 'Fulton': {'NNP': 14}, 'County': {'NNP': 7}, 'Grand': {'NNP': 1}, 'Jury': {'NNP': 1}, 'said': {'VBD': 18}, 'Friday': {'NNP': 3}......
    
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
    
    # The below code segment forms a dictionary of tags and thier values and sorts them which looks as follows : : [('NN', 261), ('DT', 191), ('NNP',188), ('IN', 185), ('NNS', 92), ('JJ', 75), ('VB', 73), ('VBD', 67), ('VBN', 54), ('TO', 39)......
    
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
    
    # The below code segment takes the most frequent tag and assigns it to all words and compares with the original list tags
    # accuarcy = matched tags/total tags
    # I got an accuracy of  17.193675889328063 after assigning 'NN' to all the words which is the most frequent tag
    
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

    # Please place the brown snapshot txt file in the same folder as this code
    # Login to the same directory folder of this code file
    # and execute python JayaramaKapilSridhara_NLP_Assignment_2.py for executing and viewing the results

main()