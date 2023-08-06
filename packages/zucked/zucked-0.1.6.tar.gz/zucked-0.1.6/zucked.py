import json
import os
import re
from datetime import datetime
from collections import Counter



class read_messages:
    result = []
    folders = os.listdir('inbox/')
    for i in range(len(folders)):
        folder = folders[i]
        with open(f'inbox/{folder}/message_1.json', 'r') as f:
            result.append(json.load(f))


    def top_words(facebook_name):
        """
        Returns the top words sent by a Facebook user (can be sender or reciever of messages)
        Params:
        - facebook_name (string): Name of desired Facebook user
        Example:
        ```
        ms = read_messages
        ms.top_50_words('Barack Obama')
        # [('America', 2), ('president', 2), ('I', 1)]
        ```
        """
        # Making a list of every message sent by someone
        message = []
        for i in range(len(read_messages.result)):
            for m in range(len(read_messages.result[i]['messages'])):
                if read_messages.result[i]['messages'][m]['sender_name'] == facebook_name:
                    try:
                        message.append(read_messages.result[i]['messages'][m]['content'])
                    except:
                        pass

        # Removing messages facebook sent whenever someone sent a link/attachment
        stopword = 'You sent an attachment.'
        for i, sub_list in enumerate(message):
                if stopword in sub_list:
                        del message[i]


        stopword = 'You sent a link.'
        for i, sub_list in enumerate(message):
                if stopword in sub_list:
                        del message[i]

        # Removing all links someone sent (using regex)
        for i in range(len(message)):
            message[i] = re.sub(r'http\S+', '', message[i])

        # Making everything lowercase
        for i in range(len(message)):
            message[i] = message[i].lower()

        # Making a list of words from the list of messages using regex to include "don't" as a word and not seperating on apostrophes
        word_list = []
        for words in list(message):
            rgx = re.compile("([\w][\w']*\w)")
            word_list = word_list + rgx.findall(words)

        # Using counter to easily count the amount of times each word appears
        word_count = Counter(word_list)
        word_count.most_common()
        return word_count.most_common()

    def top_convos(facebook_name):
        """
        Returns the name of the reciever(s) and amount of messages sent
        Params:
        - facebook_name (string): Name of desired Facebook user (can only be message sender)
        Example:
        ```
        ms = read_messages
        ms.top_convos('Barack Obama')
        # [('Joe Biden', 72)]
        ```
        """
        participants = []
        for i in range(len(read_messages.result)):
            for m in range(len(read_messages.result[i]['messages'])):
                if read_messages.result[i]['messages'][m]['sender_name'] == facebook_name:
                        participants.append([a['name'] for a in read_messages.result[i]['participants'] if a['name']!= facebook_name])
        format_participants = [name[-1] if len(name) ==1 else name for name in list(map(tuple, participants))]

        return Counter(format_participants).most_common()

    def search_messages(facebook_name,value):
        """
        Returns the name of the reciever(s) and amount of messages sent
        Params:
        - facebook_name (string): Name of desired Facebook user (can only be message sender)
        - value (string): A word or phrase to be searched
        Example:
        ```
        ms = read_messages
        ms.search_messages('User 1', 'I love data')
        # [{'Message': 'I love data science, it is really fun',
            'Sent to': 'Zark Muckerberg',
            'Date': '2016-06-09'}]
        ```
        """
        list_messages = []
        for i in range(len(read_messages.result)):
            for m in range(len(read_messages.result[i]['messages'])):
                if read_messages.result[i]['messages'][m]['sender_name'] == facebook_name:
                    if 'content' in read_messages.result[i]['messages'][m] and value in read_messages.result[i]['messages'][m]['content']:
                        date_ms = read_messages.result[i]['messages'][m]['timestamp_ms']/1000
                        date = str(datetime.fromtimestamp(date_ms))[:-7]
                        if len(read_messages.result[i]['participants']) <=2:
                            particpants = read_messages.result[i]['participants'][0]['name']
                        else:
                            particpants = read_messages.result[i]['thread_path'][6:-11]
                        words ={}
                        words['Message'] = read_messages.result[i]['messages'][m]['content']
                        words['Sent to'] = particpants
                        words['Date'] = date
                        list_messages.append(words)


        return list_messages
