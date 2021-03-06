Introduction
============

Telegram-bot-compiler is, as the name suggests, a telegram bot that compiles and executes code. It takes pastebin urls from messages, compiles and executes the code in a Docker container and pipes the output to a telegram message.

Usage
-----

Clone the repository by executing the following commands:

```
git clone  https://github.com/flammified/telegram-compile-bot.git
pip install -r requirements.txt
```


Then put your telegram http token in file called token.txt and edit the host in the code. Afterwards run:

```
python main.py
```

Otherwise, if you do not want to host it yourself, you can try it [here](https://telegram.me/compile_bot). This link will open using the Telegram client.
