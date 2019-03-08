# Jayarama Kapil Sridhara

import string
def Word_counter(sentence):
    # First tokenize words and punctuations and forming a resulting list
    result_list = []
    word = ''
    for char in sentence:
        if char not in string.whitespace:
            if char not in string.ascii_letters:
                if word:
                    result_list.append(word)
                result_list.append(char)
                word = ''
            else:
                word = ''.join([word, char])
        else:
            if word:
                result_list.append(word)
                word = ''

    # As a final list of words and punctuations and other special characters is formed forming a dictionary words and their counts
    counts = dict()
    for word in result_list:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    # Returning top 10 most frequent words or punctuations and their counts
    print('The most frequent words/punctuations in given paragraph are:')
    
    return (sorted(counts.items(), key=lambda kv: kv[1], reverse=True))[:10]

Text = 'Whales are marine mammals of order Cetacea which are neither dolphins - members, in other words, of the families delphinidae or platanistoidae - nor porpoises. They include the blue whale, the largest animal ever to have lived. Orcas, colloquially referred to as "killer whales", and pilot whales have whale in their name but for the purpose of classification they are actually dolphins. For centuries, whales have been hunted for meat and as a source of valuable raw materials. By the middle of the 20th century, large-scale industrial whaling had left many populations severely depleted, rendering certain species seriously endangered.'

print(Word_counter(Text))