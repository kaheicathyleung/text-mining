from ctypes.wintypes import PLARGE_INTEGER
from mediawiki import MediaWiki
import string
import sys
from unicodedata import category
import fuzzywuzzy
from fuzzywuzzy import fuzz


def wiki_content(topic):
    """
    This function takes a paramter topic, which is the particular title of
    the article that we would like to access. Then, it would fetch the article
    and return a string with the content in it.
    """
    wikipedia = MediaWiki()
    article = wikipedia.page(topic)
    return article.content


def word_freq(topic):
    """This function takes a paramter topic, which is the particular title of
    the article that we would like to access. Then it would return a dictionary
    where the keys are words that appear and the values are frequencies of words
    in the text content. (only show words that appear more than 10 times in the text)
    """
    text = wiki_content(topic)
    dict = {}

    strippables = ''.join(
        [chr(i) for i in range(sys.maxunicode)
         if category(chr(i)).startswith("P")]
    )

    for word in text.split():
        word = word.strip(strippables)
        word = word.lower()

        # update the dictionary
        dict[word] = dict.get(word, 0)+1

    new_dict = {}
    for key in dict:
        if dict[key] > 10:
            new_dict[key] = dict[key]

    return new_dict


def total_words(dict):
    """Returns the total of the frequencies in the dictionary"""
    return sum(dict.values())


def different_words(dict):
    """Returns the number of different words in a dictionary"""
    return len(dict)


def most_common(dict, excluding_stopwords=True):
    """
    Make a list of word-freq pairs in descending order of frequency. Take two parameters:

    dict: map from word to frequency
    excluding_stopwords: a boolean value. If it is True, do not include any stopwords in the list.

    returns: list of (frequency, word) pairs
    """

    freq_list = []

    file = open('stopwords.txt', encoding='utf8')
    stopwords_dict = {}
    for line in file:
        for word in line.split():
            stopwords_dict[word] = stopwords_dict.get(word, 0)+1
    stopwords = list(stopwords_dict.keys())
    # print(stopwords)
    for word, freq in dict.items():
        if excluding_stopwords:
            if word in stopwords:
                continue

        freq_list.append((freq, word))
    freq_list.sort(reverse=True)
    return freq_list


def print_most_common(dict, num):
    """
    Print the most common words in the text and their frequencies.
    dict: map from word to frequency
    num: number of words to print
    """
    t = most_common(dict, True)
    print('The most common words are:')
    for freq, word in t[:num]:
        print(word, '\t', freq)


def subtract(d1, d2):
    """
    Returns a dictionary with all keys that appear in d1 but not d2.
    d1 and d2 are both dictionaries
    """
    res = {}
    for key in d1:
        if key not in d2:
            res[key] = None
    return res


def text_similarity(article1, article2):
    """
    This function takes two paratmers, which are both texts in string that fetch from wikipedia for the two topics chose, 
    then the function computes the similarity of two texts, and prints the similarity ratio between two strings, token sort 
    ratio and token set ratio between two strings. 
    """
    # Learn from https://towardsdatascience.com/string-matching-with-fuzzywuzzy-e982c61f8a84
    # The article introduces string matching in Python with FuzzyWuzzy Library
    # "Ratio" calculate levenshtein distance similarity ratio between two strings
    ratio = fuzz.ratio(article1.lower(), article2.lower())
    print(
        f'The Levenshtein distance similarity ratio between Blackpink\'s content and BTS\'s content is {ratio}%.')

    # "Token Sort Ratio" would first tokenize the strings, change capitals to lowercase, and remove punctuation.
    # Then it would sorts the strings alphabetically and then joins together, and lastly, calculate the similarity ratio.
    ratio2 = fuzz.token_sort_ratio(article1, article2)
    print(
        f'The Levenshtein distance similarity ratio between Blackpink\'s content and BTS\'s content is {ratio2}%.')

    # "Token Set Ratio" is similar to token sort ratio, except that it is more useful when two strings have different kengths.
    ratio3 = fuzz.token_set_ratio(article1, article2)
    print(
        f'The Levenshtein distance similarity ratio between Blackpink\'s content and BTS\'s content is {ratio3}%.')


def main():
    topic1 = "Blackpink"
    topic2 = "BTS"
    article1 = wiki_content(topic1)
    article2 = wiki_content(topic2)
    dict1 = word_freq(topic1)
    dict2 = word_freq(topic2)
    print(dict1)
    print(dict2)
    print('Total number of words in Blackpink\'s page are:', total_words(dict1))
    print('Number of different words in Blackpink\'s content are:',
          different_words(dict1))
    print('Total number of words in BTS\'s page are:', total_words(dict2))
    print('Number of different words in BTS\'s content are:', different_words(dict2))

    print(most_common(dict1,excluding_stopwords=True))
    print(most_common(dict2,excluding_stopwords=True))

    print_most_common(dict1,30)
    print_most_common(dict2,30)

    diff = subtract(dict1, dict2)
    print('The words in the Blackpink\'s page but not in BTS\'s page are:')
    for word in diff.keys():
        print(word)

    text_similarity(article1, article2)


if __name__ == "__main__":
    main()
