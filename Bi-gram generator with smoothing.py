# -*- coding: utf-8 -*-
import re
import io
from collections import Counter
from collections import defaultdict
from collections import OrderedDict

def CleanText(Inputfile):
    """
    This function cleans the input text file

    """
    Regex = re.compile(r"([A-Z$]+ [\w]+)")
    with open(Inputfile , 'r+') as f:
        sentence = ''
        for line in f:
            if  re.search('(TOP END_OF_TEXT_UNIT)',line):
                continue
            else:
                tagWord = ' '.join(Regex.findall(line))
                sentence = sentence +' '+ tagWord 
    return sentence

def PureText(text):
    """
    This function extracts clean text from the input

    """
    puretext =[]
    data = text.split()
    data = [word.lower() for word in data]
    for i in range(len(data)):
        if i%2!=0:
            puretext.append(data[i])
    return puretext

def WordCounter(text):
    """
    This function builds words and its counts in a dictionary

    """
    word_count= {}
    for i in range(len(text)):
        if text[i] in word_count:
            word_count[text[i]] += 1
        else:
            word_count[text[i]] = 1   
    return OrderedDict(sorted(word_count.items(), key=operator.itemgetter(1), reverse=True))

def bigrams(input_list):
    """
    This function builds bigrams from the input text

    """
    return list(zip(input_list, input_list[1:]))

def smoothed_bigram(word_count, bi_gram):
    """
    This function smooths the bigrams using zipfs law

    """
    smoothed_bigram = {}
    voc_size = len(word_count)
    for bi_gram_u in bi_gram:
        smoothed_bigram[bi_gram_u] = (bi_gram[bi_gram_u]+1)/(word_count[bi_gram_u[0]]+voc_size)

    return smoothed_bigram

def visualize_zip_f(word_count):
    """
    This function plots the graph of zips law

    """
    title = "Frequency Distribution of Words"
    x_label = "Word Rank"
    y_label = "Frequency"
    freq = []
    i=0
    rnk = np.arange(0, len(word_count), 1)
    
    for word in word_count:
        freq.append(word_count[word])
        
    fig = plt.figure()
    plt.plot(rnk, freq)
    fig.suptitle(title, fontsize=15)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=10)
    plt.show()

def test_bigram(text):
    """
    This function builds bigrams for test input
    """
    text = text.lower()
    text_splits = text.split(" ")
    
    bigram_str = {}
    for i in range(len(text_splits)-1):
        if (text_splits[i], text_splits[i+1]) in bigram_str:
            bigram_str[text_splits[i], text_splits[i+1]] +=1 
        else:
            bigram_str[text_splits[i], text_splits[i+1]] = 1
            
    return bigram_str

def bigram_compare(bigram_str,bi_gram, word_count):
    """
    This function builds  bigram dictionary and smooth bigram dictionary

    """
    bigram_dict = {}
    bigram_dict_smoothed = {}
    vocabulary_size = len(word_count)
    
    for pair in bigram_str:
        if pair in bi_gram:
            bigram_dict[pair] = bi_gram[pair]/word_count[pair[0]]
            bigram_dict_smoothed[pair] = (bi_gram[pair]+1)/(word_count[pair[0]]+vocabulary_size)
        else:
            if pair[0] in word_count:
                bigram_dict[pair] = 0
                bigram_dict_smoothed[pair] = 2/(word_count[pair[0]]+vocabulary_size)
            else:
                bigram_dict[pair] = 0
                bigram_dict_smoothed[pair] = 2/(vocabulary_size)
       
    return bigram_dict, bigram_dict_smoothed

def ComapareBigrams(bigram_dict, bigram_dict_smoothed):
    """
    This function compares bigram dictionary and smooth bigram dictionary

    """
    for pair in bigram_dict:
        print("%25s - Raw: %0.4f, Smoothed: %0.4f"% (pair, bigram_dict[pair], bigram_dict_smoothed[pair]))

def main():
    """
    Main function

    """

    Inputfile = 'SnapshotBROWN.pos.all.txt'
    text = CleanText(Inputfile)
    text = PureText(text)
    word_count = WordCounter(text)
    bi_gram = bigrams(text)
    bigram_count = WordCounter(bi_gram)
    visualize_zip_f(word_count)
    test_bi_gram = test_bigram('A similar resolution passed in the Senate')
    raw_bigram, smoothed_bigram = bigram_compare(test_bi_gram,bigram_count, word_count)
    print('--------------------------------------------')
    print(' Bigrams Grammer Before and After Smoothing ')
    print('--------------------------------------------')
    ComapareBigrams(raw_bigram, smoothed_bigram)

if __name__== "__main__":

  main()