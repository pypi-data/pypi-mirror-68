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

    stopwords = ['i','me','my','myself','we','our','ours','ourselves','you',"you're","you've","you'll","you'd",'your','yours','yourself','yourselves','he','him','his',
    'himself','she',"she's",'her','hers','herself','it',"it's",'its','itself','they','them','their','theirs','themselves','what','which','who','whom','this','that',
    "that'll",'these','those','am','is','are','was','were','be','been','being','have','has','had','having','do','does','did','doing','a','an','the','and','but','if',
    'or','because','as','until','while','of','at','by','for','with','about','against','between','into','through','during','before','after','above','below','to','from',
    'up','down','in','out','on','off','over','under','again','further','then','once','here','there','when','where','why','how','all','any','both','each','few','more',
    'most','other','some','such','no','nor','not','only','own','same','so','than','too','very','s','t','can','will','just','don',"don't",'should',"should've",'now','d',
    'll','m','o','re','ve','y','ain','aren',"aren't",'couldn',"couldn't",'didn',"didn't",'doesn',"doesn't",'hadn',"hadn't",'hasn',"hasn't",'haven',"haven't",'isn',
    "isn't",'ma','mightn',"mightn't",'mustn',"mustn't",'needn',"needn't",'shan',"shan't",'shouldn',"shouldn't",'wasn',"wasn't",'weren',"weren't",'won',"won't",'wouldn',
    "wouldn't","i'm"]
    def top_words(facebook_name, stop_words=True, period='all time'):
        """
        Returns the top words sent by a Facebook user (can be sender or reciever of messages)
        Params:
        - facebook_name (string): Name of desired Facebook user
        - stop_words (Bool): Will the words returned include stopwords
        - period (string): 'all time' for all messages or a year, i.e '2016' for top words that year
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
                if period == 'all time':
                    if read_messages.result[i]['messages'][m]['sender_name'] == facebook_name:
                        try:
                            message.append(read_messages.result[i]['messages'][m]['content'])
                        except:
                            pass
                else:
                    if read_messages.result[i]['messages'][m]['sender_name'] == facebook_name and str(datetime.fromtimestamp(read_messages.result[i]['messages'][m]['timestamp_ms']/1000))[:4] == period:
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

        # Making a list of words from the list of messages
        word_list = [word for sentence in message for word in sentence.split()]

        # Removing stop_words
        if stop_words==False:
            words = [w for w in word_list if not w in read_messages.stopwords]
        else:
            words = word_list

        # Using counter to easily count the amount of times each word appears
        word_count = Counter(words)
        word_count.most_common()
        return word_count.most_common()

    def top_convos(facebook_name, period='all time'):
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
                if period == 'all time':
                    if read_messages.result[i]['messages'][m]['sender_name'] == facebook_name:
                        participants.append([a['name'] for a in read_messages.result[i]['participants'] if a['name']!= facebook_name])
                        format_participants = [name[-1] if len(name) ==1 else name for name in list(map(tuple, participants))]
                else:
                    if read_messages.result[i]['messages'][m]['sender_name'] == facebook_name and str(datetime.fromtimestamp(read_messages.result[i]['messages'][m]['timestamp_ms']/1000))[:4] == period:
                        participants.append([a['name'] for a in read_messages.result[i]['participants'] if a['name']!= facebook_name])
            format_participants = [name[-1] if len(name) ==1 else name for name in list(map(tuple, participants))]
        return Counter(format_participants).most_common()

    def search_messages(facebook_name,value):
        """
        Returns the name of the message reciever(s) and amount of messages sent
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

    def format_top_words(facebook_name, input_list, year):
        """
        Returns a dictionary with the year and names and counts of words inputed for a specific Facebook User
        Params:
        - facebook_name (string): Name of desired Facebook user
        - input_list (list): A list of words that you want the count of for a certain year
        - year (string): The year that the messages will be counted in
        Example:
        ```
        ms = read_messages
        ms.format_top_words('Jordan Milne', ['i','love','data','man'], '2014')
        # {'2014': {'i': 75, 'love': 70, 'man': 17, 'data': 10}}
        ```
        """
        message = []
        format_dict = {}
        for i in range(len(read_messages.result)):
            for m in range(len(read_messages.result[i]['messages'])):
                if read_messages.result[i]['messages'][m]['sender_name'] == facebook_name and str(datetime.fromtimestamp(read_messages.result[i]['messages'][m]['timestamp_ms']/1000))[:4] == year:
                    try:
                        message.append(read_messages.result[i]['messages'][m]['content'])
                    except:
                        pass
        final_dict = {}
        word_list = [word for sentence in message for word in sentence.split() if word in input_list]
        # Count the number of times each word of input_list appears in word_list
        counts = Counter(word_list)
        [counts.setdefault(key, 0) for key in input_list]
        final_dict[year] = dict(counts)
        return final_dict
