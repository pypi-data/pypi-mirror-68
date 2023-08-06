# snoozingmail
A minimal python3 wrapper for the Gmail API that exposes basic message reading, modifying, and sending capabilities.

# install
```
pip install snoozingmail
```

# usage
- You'll first need to create a Cloud Platform project enabled with the python Gmail API, and download the *credentials.json* file. To do that follow Google's [quickstart](https://developers.google.com/gmail/api/quickstart/python)
- Create a new `Snoozin` object with the path to your *credentials.json* file like so:
    ```python
    snoozingmail.Snoozin("./credentials.json")
    ```
- The first instantiation of `Snoozin` with your *credentials.json* file will prompt you to visit a url to pick what gmail account to give snoozin access to. A *token.pickle* file will be then be created for automatic authentication with the chosen account for future instantiations.

## example
Print message body of first starred message in inbox
```python
import snoozingmail

snoozin = snoozingmail.Snoozin("./credentials.json")
msg_ids = snoozin.get_labeled_msgs(['STARRED', 'INBOX'])
body_text = snoozin.get_msg_body(msg_ids[0])
print(body_text)

```

# docs
- Full documentation of snoozingmail module: https://snoozingmail.readthedocs.io/en/latest/
- The core gmail interfaces were based off of the python 2 Users.messages section of the Gmail api: https://developers.google.com/gmail/api/v1/reference/users/messages
