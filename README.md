# discord-bot-project
Discord project I created to keep track of information for a personal server. 

## Using this bot
>NOTE: This bot is not meant for use outside of the personal enviornment I created it in.

This code runs a discord bot using a token generated from the official discord developer portal. The token for this bot is stored in a file on my personal computer and is not present in this repository.
To recieve your own token you can follow the instructions [here](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/).

Currently, this bot only has functionality for the following commands:
- ?help
- ?debts

### ?help
Displays the list of commands this bot has.

### ?debts *[optional list of names]*
Scrapes a certain google sheets spreadsheet and displays any money each individual may owe another.\
By default, all debts will be returned, an optional space delimited list of names can be included with the command to return only those indivual's debts.
> ex. ?debts John Panda Joe\
> This will return only the debts that John, Panda, and Joe owe.
