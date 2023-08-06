<h3 align="center">
  <img src="https://raw.githubusercontent.com/Jordan-Milne/zucked/master/icon.png" height="300px" alt="zucked">
</h3>
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
* Search a word or phrase that might have sent or recieved to see the message the word or phrase was in as well as who sent it and when



## Install


The source code is currently hosted on GitHub at: https://github.com/Jordan-Milne/zucked

latest released version are available at the [Python package index (PyPI)](https://pypi.org/project/zucked/)

`pip install zucked`


## Tutorial

* **Downlaod your [Facebook Messenger data](https://www.zapptales.com/en/download-facebook-messenger-chat-history-how-to/)**

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

call `top_words(facebook_name)` on `ms` to return an ordered list of the most common words the user sent and how many times they sent it:

Example:
```
ms.top_words('Jordan Milne')
```
Returns:

```
[('I', 3), ('love', 2), ('data', 1)]
```

*This method works for top words you have sent **and** top words you have recieved from a certain user*

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
