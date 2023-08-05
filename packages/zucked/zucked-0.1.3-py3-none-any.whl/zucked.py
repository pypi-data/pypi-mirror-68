# import glob
# import itertools
import json
import os
import re

# import altair as alt
# import pandas as pd
from collections import Counter
# import nltk
# from nltk.corpus import stopwords
#
# nltk.download('stopwords')


class read_messages():
    result = []
    folders = os.listdir('inbox/')
    for i in range(len(folders)):
        folder = folders[i]
        with open(f'inbox/{folder}/message_1.json', 'r') as f:
            result.append(json.load(f))


    def top_50_words(facebook_name):
        # Making a list of every message sent by me
        message = []
        for i in range(len(read_messages.result)):
            for m in range(len(read_messages.result[i]['messages'])):
                if read_messages.result[i]['messages'][m]['sender_name'] == facebook_name:
                    try:
                        message.append(read_messages.result[i]['messages'][m]['content'])
                    except:
                        pass

        # Removing messages facebook sent whenever I sent a link/attachment
        stopword = 'You sent an attachment.'
        for i, sub_list in enumerate(message):
                if stopword in sub_list:
                        del message[i]


        stopword = 'You sent a link.'
        for i, sub_list in enumerate(message):
                if stopword in sub_list:
                        del message[i]

        # Removing all links I sent (using regex)
        for i in range(len(message)):
            message[i] = re.sub(r'http\S+', '', message[i])

        # Making everything lowercase
        for i in range(len(message)):
            message[i] = message[i].lower()

        # Making a list of words from my list of messages using regex to include "don't" as a word and not seperating on apostrophes
        word_list = []
        for words in list(message):
            rgx = re.compile("([\w][\w']*\w)")
            word_list = word_list + rgx.findall(words)

        # # Removing stopwords
        # stop_words = stopwords.words('english')
        # stop_words.append("i'm")
        # words = [w for w in word_list if not w in stop_words]

        # Using counter to easily count the amount of times each word appears
        word_count = Counter(word_list)
        word_count.most_common()

        # my top 10 words over ALL years
        # df = pd.DataFrame([word for word in word_count.most_common()[:50] ],columns= ['word','count'])
        return word_count.most_common()[:50]
