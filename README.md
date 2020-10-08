# IMDB-Twitch-Bot

This is a simple twitch bot written in Python using Tkinter for interface, Socket for accessing Twitch. The IMDB functions use HTML parsing to collect all the informations and does not use any IMDB API's.

What to Edit:<br/>
The File bot.py has 4 variables that need updating.<br/>
NICK is for the main Channel the bot wants to be in.<br/>
PASS is for the main Channel.<br/>
BOTNICK is for the bot.<br/>
BOTNICK is for the bot.<br/>

How to compile (Windows):<br/>
Make sure to have pyinstaller and updated.<br/>
Command: pyinstaller --onefile app.py --noconsole --name TwitchBot<br/>
This will create an app in the 'dist' folder that can be opened. Windows might say this app is a virus but you can just allow it to run.

## NOTE  
Make sure to make bot account (second account) a moderator. As twitch blocks a user to put in the same message twice but if the message is from a moderator, it does not matter.
