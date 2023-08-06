<p align="center">
  <a href="https://github.com/Jordan-Milne/zucked"><img alt="Dependencies"src="https://raw.githubusercontent.com/Jordan-Milne/zucked/master/icon.png"></a>
<p>
<p align="center">   
  <a href="https://github.com/Jordan-Milne/zucked/blob/master/setup.py"><img alt="Dependencies"src="https://img.shields.io/badge/dependencies-0-brightgreen"></a>
  <a href="https://travis-ci.org/github/Jordan-Milne/zucked"><img alt="Travis" src="https://img.shields.io/travis/jordan-milne/zucked"></a>   
  <a href="https://pypi.python.org/pypi/zucked"><img alt="PyPI" src="https://img.shields.io/pypi/v/zucked"></a>   
  <a href="https://pypi.org/project/zucked/"><img alt="Downloads" src="https://img.shields.io/pypi/dm/zucked"></a>
</p>


-----------

# zucked: analyze your Facebook Messenger data

## What is it?

zucked is a quick and easy way to veiw your facebook messenger data.



## Main Features

* Easy viewing of your most used words on Facebook Messenger
* See another facebook users most sent words to you
* Check the amount of messages you have sent a person or group
* Search a word or phrase that you might have sent or recieved to see: The message the word or phrase was in, as well as who sent it and when the message was sent



## Install


The source code is currently hosted on GitHub at: https://github.com/Jordan-Milne/zucked

The latest released version is available at the [Python package index (PyPI)](https://pypi.org/project/zucked/)

`pip install zucked`


## Tutorial

* **Downlaod your Facebook Messenger data ([How to](https://www.zapptales.com/en/download-facebook-messenger-chat-history-how-to/))**
  * When choosing file type make sure it is JSON and not HTML

* Create a python file in the **same directory** as the "inbox" folder from your download -  **not inside** the inbox folder


### Import

To import zucked, type:

```
import zucked as zd
```

### read_messages

save `read_messages` as a variable, which we will be calling methods on later.

Example:
```
ms = zd.read_messages
```

### top_words()

call `top_words(facebook_name, stop_words=True, period='all time')` on `ms` to return an ordered list of the most common words the user sent and how many times they sent it:
*This method works for top words you have sent **and** top words you have recieved from a certain user*
Example:
```
ms.top_words('Jordan Milne')
```
Returns:

```
[('I', 3), ('love', 2), ('data', 1)]
```
*If you want stop words filtered out, ([what are stop words](https://en.wikipedia.org/wiki/Stop_words)) and just the top words for a certain year then the method would simply be:*
```
ms.top_words('Jordan Milne', stop_words=False, period='2016')
```


### top_convos

call `top_convos(facebook_name)` on `ms` to return an ordered list of the name(s) of the person or group and the amount of messages you sent to that person or group:

Example:
```
ms.top_convos('Jordan Milne')
```
Returns:
```
[('User 1', 33),
 ('User 2', 21)]
```

*If you want the top conversations for a certain year then the method would simply be:*
```
ms.top_words('Jordan Milne', period='2016')
```


### search_messages()

call `search_messages(facebook_name, value)` on `ms` to return a list that has the full message containing the word or phrase input as `value`, who the message was sent to, and the date and time the message was sent.

Example:
```
ms.search_messages('Jordan Milne', 'hello')
```
Returns:
```
[{'Message': 'I'm sorry but, hello world',
  'Sent to': 'Auston Matthews',
  'Date': '2019-06-09 11:46:54'}]
```

*This method works for messages you have sent **and** messages you have recieved from a certain user*

### format_top_words()
call `format_top_words(facebook_name, input_list, year)` on `ms` to return a nested dictionary with the year and counts of the list of words that the user inputs that is specifically formatted for plotting.

Example:
```
ms.format_top_words('Jordan Milne', ['Matthews','Tavares','Marner','Andersen'], '2019')
```
Returns:
```
{'2019': {'Matthews': 75, 'Andersen': 70, 'Marner': 17, 'Tavares': 10}}

```
Now for the fun part. If you want to see how often you used your top 5 all time words each year it can be done in a few simple steps.

Get all years into the same dictionary using this for loop:
```
example={}
for i in range(2010,2021):
    example.update(ms.format_top_words('Jordan Milne',['Matthews','Tavares','Marner','Andersen'], str(i)))
```

Now that we have the data collected and organized we are ready to plot:

```
import matplotlib.pyplot as plt

# get inner keys
inner_keys = list(example.values())[0].keys()

# x-axis is the outer keys
x_axis_values = list(example.keys())

# loop through inner_keys
plt.title("Facebook Messenger Word Count")
plt.xlabel("Year")
plt.ylabel("Count");
for x in inner_keys:

    # create a list of values for inner key
    y_axis_values = [v[x] for v in example.values()]

    # plot each inner key
    plt.plot(x_axis_values, y_axis_values, label=x)
    plt.legend()
```
**The ouput should look like:**
![example](example.png)
