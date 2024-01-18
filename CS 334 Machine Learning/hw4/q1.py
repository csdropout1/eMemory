import argparse
import numpy as np
import pandas as pd
from sklearn import preprocessing
from collections import defaultdict
import time

def model_assessment(filename):
    """
    Given the entire data, split it into training and test set 
    so you can assess your different models 
    to compare perceptron, logistic regression,
    and naive bayes. 
    """
    train_ratio = 0.8 ## Dynamic
    text = []
    y_labels = []

    with open(filename, 'r') as file:
        for line in file:
            y_labels.append(int(line[0]))
            text.append(line[2:].split(' '))

    df =  pd.DataFrame({'text': text, 'y':y_labels})

    p = np.random.permutation(df.index)
    df = df.iloc[p]
    df.reset_index(drop=True, inplace=True)

    trs = int(train_ratio*df.shape[0])
    train_set, test_set = df.iloc[:trs], df.iloc[trs: df.shape[0]]
    return train_set, test_set


def build_vocab_map(traindf):
    """
    Construct the vocabulary map such that it returns
    (1) the vocabulary dictionary contains words as keys and
    the number of emails the word appears in as values, and
    (2) a list of words that appear in at least 30 emails.

    ---input:
    dataset: pandas dataframe containing the 'text' column
             and 'y' label column

    ---output:
    dict: key-value is word-count pair
    list: list of words that appear in at least 30 emails
    """
    v_map = defaultdict(int) # dictionary, but auto initializes key if not in dict.
    more_30 = []

    for email in traindf['text']:
        words = set(email) # Updates one word at most once per email, take uniques
        for word in words:
            v_map[word] += 1
            if v_map[word] > 30:
                more_30.append(word)

    more_30 = set(more_30) # remove duplicates

    # only for the filter words
    v_map = {word: count for word, count in v_map.items() if word in more_30}
    return dict(v_map), list(more_30)


def construct_binary(dataset, freq_words):
    """
    Construct email datasets based on
    the binary representation of the email.
    For each e-mail, transform it into a
    feature vector where the ith entry,
    $x_i$, is 1 if the ith word in the 
    vocabulary occurs in the email,
    or 0 otherwise

    ---input:
    dataset: pandas dataframe containing the 'text' column

    freq_word: the vocabulary map built in build_vocab_map()

    ---output:
    numpy array
    """
    list_of_records = []
    f = freq_words
    for e in range(len(dataset['text'])):
        vector = [0]*len(f)
        for w in range(len(f)):
            if f[w] in dataset['text'].iloc[e]:
                vector[w] = 1
            else:
                vector[w] = 0
        list_of_records.append(vector)
    return np.array(list_of_records)



def construct_count(dataset, freq_words):
    """
    Construct email datasets based on
    the count representation of the email.
    For each e-mail, transform it into a
    feature vector where the ith entry,
    $x_i$, is the number of times the ith word in the 
    vocabulary occurs in the email,
    or 0 otherwise

    ---input:
    dataset: pandas dataframe containing the 'text' column

    freq_word: the vocabulary map built in build_vocab_map()

    ---output:
    numpy array
    """
    print(dataset['text'].shape)
    print(len(freq_words))
    list_of_records = []
    f = freq_words
    for e in range(len(dataset['text'])):
        vector = [0]*len(f)
        for w in range(len(f)):
            vector[w] = int(list(dataset['text'].iloc[e]).count(f[w]))
        list_of_records.append(vector)
    return np.array(list_of_records)

def main():
    """
    Main file to run from the command line.
    """
    # set up the program to take in arguments from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("--data",
                        default="spamAssassin.data",
                        help="filename of the input data")
    args = parser.parse_args()
    a = model_assessment(args.data)
    m = build_vocab_map(a[0])

    print(m[1]) # Recorded for later

    data = construct_binary(a[0], m[1])
    data_c = construct_count(a[0], m[1])

    data_x = pd.DataFrame(data)
    data_y = pd.DataFrame(a[0]['y'])
    data_x.to_csv("xTrain.csv", index=False)
    data_y.to_csv("yTrain.csv", index=False)

    data_xx = pd.DataFrame(data_c)
    data_yy = pd.DataFrame(a[0]['y'])
    data_xx.to_csv("xTrain-c.csv", index=False)
    data_yy.to_csv("yTrain-c.csv", index=False)
    
    data2 = construct_binary(a[1], m[1])
    data2_c = construct_count(a[1], m[1])

    data2_x = pd.DataFrame(data2)
    data2_y = pd.DataFrame(a[1]['y'])
    data2_x.to_csv("xTest.csv", index=False)
    data2_y.to_csv("yTest.csv", index=False)

    data2_xx = pd.DataFrame(data2_c)
    data2_yy = pd.DataFrame(a[1]['y'])
    data2_xx.to_csv("xTest-c.csv", index=False)
    data2_yy.to_csv("yTest-c.csv", index=False)

if __name__ == "__main__":
    main()
