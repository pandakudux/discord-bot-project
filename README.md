# discord-bot-project
A discord bot I created to keep track of information for a personal server. 

## Using this bot
>NOTE: This bot is not meant for use outside of the personal enviornment I created it in.

This code runs a discord bot using a token generated from the official discord developer portal. The token for this bot is stored in a file on my personal computer and is not present in this repository.
To recieve your own token you can follow the instructions [here](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/).

Currently, this bot only has functionality for the following commands:
- ?help
- ?debts

### ?help
Displays the list of commands this bot has.

> ex. ?help\
> ![Example of ?help functionality](/assets/help_functionality.png)

### ?debts *[optional list of names]*
Scrapes a certain google sheets spreadsheet and displays any money each individual may owe another.\
By default, all debts will be returned, an optional space delimited list of names can be included with the command to return only those indivual's debts.
> \**all names changed for privacy reasons*\
> ex. ?debts\
> ![Example of ?debts default functionality](/assets/debts_default_functionality.png)\
> ex. ?debts John Panda Joe\
> ![Example of ?debts with a list of names](/assets/debts_extended_functionality.png)\

## main.py
This file contains the code that runs the discord bot as well as contains its commands. Note that the token for the bot is stored on a file on my personal computer, if you wanted to use this code then you must use your own discord project token. 

## debt_calc.py
This code is the backend for the functionality behind the ?debt command. This code access the google documents and google sheets APIs to scrape the information off of a specified spreadsheet. It creates a nested dictionary structure which is used to generate the embeds sent to the discord server. To access the APIs, an api key must be acquired from the google developers portal, if you want to use this code you must replace the file path in the code to the path of your own API key. Google developer API keys can be acquired by following [this guide](https://cloud.google.com/docs/authentication/api-keys#:~:text=on%20the%20project.-,Creating%20an%20API%20key,displays%20your%20newly%20created%20key.).

> NOTE: Much of this code is adapted from stackoverflow code I found while searching for libraries to access google sheets API information
