# coding: utf-8
# author: jayarama kapil sridhara

import re
import io
from collections import Counter
from collections import defaultdict
from collections import OrderedDict

# Cleans entire brown corpus and returns an output file with just word and their tags.
def CleanFile(In,Out):
    Regex = re.compile(r"([A-Z$]+ [\w]+)")
    with open(In , 'r+') as f:
        mylist = []
        sentence = ' '
        for line in f:
            if  re.search('(TOP END_OF_TEXT_UNIT)',line):
                sentence = sentence + '\n'
            else:
                tagWord = ' '.join(Regex.findall(line))
                sentence = sentence +' '+ tagWord 
    with open(Out,mode ='a') as outfile:
        outfile.write(sentence)

# This function returns a Hash of Hash Dictionary with each word, the possible tag of the word and their counts--> {word:{tag1:count1,tag2:count2..}}
def HashOfHash():
    global hash_dict
    with open(TrainingOutputfile, 'r') as f:
        data = f.read()
        data = data.split()
        word_dict= defaultdict(lambda: [])
        for i in range(0,len(data)):
            if i%2!=0:
                word_dict[data[i]].append(data[i-1])
    hash_dict = {k: dict(Counter(v)) for k, v in word_dict.items()}  


# Using hash of hashes function to train a baseline lexicalized statistical tagger on the entire BROWN corpus.
def Statistical_tagger():
    global trained_tagger
    trained_tagger = {}
    for word,taglist in hash_dict.items():
        frequent_tag = sorted(taglist.items(), key=lambda x: x[1],reverse=True)[0][0]
        trained_tagger[word] = frequent_tag


# Using the baseline lexicalized statistical tagger to tag all the words in the SnapshotBROWN file.
def TagSnapshot():
    global Evaluated_tags
    global Original_tags
    global Unknown_Words
    with open(TestOutputFile, 'r') as f:
        data = f.read()
        data = data.split()
        Original_tags = []
        Evaluated_tags = []
        Unknown_Words = []
        for i in range(0,len(data)):
            if i%2!=0:
                if data[i] not in trained_tagger.keys():
                    Unknown_Words.append(data[i])
                    Evaluated_tags('TAG-NOT-FOUND')
                else:
                    Original_tags.append(data[i-1])
                    Evaluated_tags.append(trained_tagger[data[i]])  

# This funciton returns the evaluation parameters of the baseline lexicalised tagger such as accuracy,error and number of words that are not tagged
def EvaluateTagger():
    count = 0
    for i in range(0,len(Evaluated_tags)):
        if Evaluated_tags[i]==Original_tags[i]:
            count = count+1
    accuracy = float(count*100)/len(Evaluated_tags)
    print('The Performance  of Trained Tagger on Snapshot Brown file: ')
    print(' ------------------------------------------------------- ')
    print('The accuracy of the Tagger                 :    {}{}'.format(accuracy,'%'))
    error = (100-accuracy)
    print('The error of the Tagger                    :    {}{}'.format(error,'%'))
    print('The number of words that are not tagged    :    {}  '.format(len(Unknown_Words)))
    

# This function adds few rules to handle unknown words for the base line lexicalised tagger
def Tag_New_Words(word):

    modals = ["can", "could", "may", "might", "will", "would", "shall", "should", "must"]
    wh_determiner = ["what", "which", "whose", "whatever", "whichever"]
    articles = ["a", "an", "the"]
    personal_pronoun = ["I","me", "you", "he", "him", "she", "her", "it", "we", "us", "you", "they", "them"]
    possessive_pronoun = ["mine", "yours", "his", "hers", "ours", "yours", "theirs"]
    
    if word.lower() in modals:
        return "MD"
    elif word.lower() in wh_determiner:
        return "WDT"
    elif word.lower() in articles:
        return "DT"
    elif (word or word.lower()) in personal_pronoun:
        return "PP"
    elif word.lower() in possessive_pronoun:
        return "PP$"
    elif word[len(word)-2:] == "ss":
        return "NN"
    elif word[len(word)-2:] == "ed":
        return "VBN"
    elif word[len(word)-3:] == "ing":
        return "VBG"
    elif word[len(word)-2:] == "ly":
        return "BB"
    elif word+"ly" in trained_tagger.keys():
        return "JJ"
    elif word[len(word)-2:] == "us":
        return "JJ"
    elif word[len(word)-3:] == "ble":
        return "JJ"
    elif word[len(word)-2:] == "ic":
        return "JJ"
    elif ((word[:2] == "un") and (word[2:] in trained_tagger.keys())):
        return "JJ"
    elif word[len(word)-3:] == "ive":
        return "JJ"
    elif word[len(word)-1:] == "s":
        return "NNS"
    elif word.isdigit():
        return "CD"
    elif word == "+" or word == "%" or word == "&":
        return "SYM"
    elif word == "{" or word == "(" or word == "[" or word == "<":
        return "("
    elif word == "}" or word == ")" or word == "]" or word == ">":
        return ")"
    elif word == "," or word == ";" or word == "-" or word == "-":
        return ","
    elif word == "." or word == "!" or word == "?":
        return "."
    elif word == '$' or word == '#' or word == ',':
        return word
    elif (word == "\"" or word == "\"" or word == '”' or word == '“' or word == '’' or word == "'" or word == "'" or word == '`' or word == '""' or word == "''" ):
        return word
    elif (word.isupper() and len(word)>2):
        return "NNP"
    elif (word[:1]).isupper() and len(word)>1 and (word[:2]).lower()!="wh" and (word[:2]).lower()!="th":
        return "NNP"
    else:
        return "<NONE>"
    

# This function cleans the news article that is used for testing of lexicalised tagger with new rules added
def CleanNewsArticle(In):
    global text
    with io.open(In,'r',encoding = 'utf-8') as f:
        text = f.read()
        text = re.findall(r"[\w]+|[^\s\w]", text)
        text = [x.encode('UTF8') for x in text]
        

# This function Tags all the words,punctutations and others in the Newspaper article
def TagNewsPaper():
    global TagContent,Count_Total_Words, Count_Known_Words, Count_New_Words,Count_New_Words_Tagged, Count_New_Words_NotTagged
    Count_Total_Words = len(text)
    Count_Known_Words, Count_New_Words,Count_New_Words_Tagged, Count_New_Words_NotTagged = 0,0,0,0
    TagContent = OrderedDict()
    for word in text:
        if word in trained_tagger.keys():
            Count_Known_Words +=1
            TagContent[word] = trained_tagger[word]
        else:
            Count_New_Words +=1
            TagContent[word] = Tag_New_Words(word)
            if TagContent[word] == "<NONE>":
                Count_New_Words_NotTagged += 1
            else:
                Count_New_Words_Tagged +=1


# This function displays the words and tags of the Newspaper file by using the trained tagger with added rules               
def DisplayNewspaperTags():
    print('Tagging Words in Newspaper using New Tagger ')
    for key,value in TagContent.items():
        if key in trained_tagger.keys():
            print("Word (Known-Tagged)            : %6s      %s"% (value, key))
        
        elif Tag_New_Words(key) != "<NONE>":
            print("Word (UnKnown-Tagged)          : %6s      %s"% (value, key))
            
        elif Tag_New_Words(key) == "<NONE>":
            print("Word (UnKnown-Not-Tagged)      : %6s      %s"% (value, key))


# This fucntion prints the Performance metrics of the New Tagger with added rules.            
def PerformanceNewTagger():
    Percentile_Known_Words = float(Count_Known_Words*100)/Count_Total_Words
    Percentile_New_Words = float(Count_New_Words*100)/Count_Total_Words
    Percentile_New_Words_Tagged = float(Count_New_Words_Tagged*100)/Count_New_Words
    Percentile_New_Words_Not_Tagged = float(Count_New_Words_NotTagged*100)/Count_New_Words
    
    print('The Performance of Trained Tagger on Newspaper file: ')
    print(' ------------------------------------------------------- ')
    print('Total Number of Words                             : {}'.format(Count_Total_Words))
    
    print('Tagged Words Known (percentile among all words)   : {} ({}%)'.format(Count_Known_Words,Percentile_Known_Words))

    print('New Words(percentile among all words)             : {} ({}%)'.format(Count_New_Words,Percentile_New_Words))

    print('Words Tagged(percentile among all new words)      : {} ({}%)'.format(Count_New_Words_Tagged,Percentile_New_Words_Tagged))

    print('Words Could Not Tag (percentile in new words)     : {} ({}%)'.format(Count_New_Words_NotTagged,Percentile_New_Words_Not_Tagged))


# Main function to run all the aove defined functions    
def main():
    
    global TrainingInputfile,TrainingOutputfile,TestInputFile,TestOutputFile,InputNewspaper
    
    TrainingInputfile = 'BROWN.pos.all'
    TrainingOutputfile = 'CleanFullBrown.txt'
    TestInputFile = 'SnapshotBROWN.pos.all.txt'
    TestOutputFile = 'CleanSnapshot.txt'
    InputNewspaper = 'Newspaper.txt'
    
    CleanFile(TrainingInputfile,TrainingOutputfile)
    HashOfHash()
    Statistical_tagger()
    CleanFile(TestInputFile,TestOutputFile)
    TagSnapshot()
    EvaluateTagger()
    print(' ------------------------------------------------------- ')
    print('\n')
    CleanNewsArticle(InputNewspaper)
    TagNewsPaper()
    DisplayNewspaperTags()
    print(' ------------------------------------------------------- ')
    print('\n')
    PerformanceNewTagger()

main()