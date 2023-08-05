
### IMPORTANT:  
### This application is not a virus and will not gain access or harm your computer, Reddit account, or anything else. Snookey2 is completely open source so you can check the .py file for all the code and see that there's nothing harmful. None of this data is stored, because I don't even know how to do that. I wouldn't even do it anyways if I knew how cause that would be really evil and ruin my reputation forever... Anyways, thank you for understanding, and have fun streaming! 

Hi!

This application was made by u/Spikeedoo and was updated by u/IOnlyPlayAsDrif!

App icon was made by Reddit.

[Join the Unofficial RPAN Discord Server for Snookey2 Support/Reporting Bugs/Suggestions/and just talking to other streamers/viewers!](https://discord.gg/3GcApfT)

Thank you for downloading Snookey!

Added:
- Discord Rich Presence
- More descriptive and better looking text
- Auto closes when getting a stream spot is successful after 1 hour
- Finally figured out how to make it a module thanks to help in the Discord!
- Retries every 2 seconds if requesting a stream spot fails with error message

(Check the Releases tab of this repo to see the full list of changes.)

[Original Snookey by u/Spikeedoo is here.](https://github.com/Spikeedoo/SnooKey)   

The text and stuff below was originally made by u/Spikeedoo (with some modifications from me):

# Snookey2
Some reddit users figured out a way to stream to RPAN (Reddit's livestreaming platform) from desktop streaming software 
(like OBS).  Project SnooKey is my attempt at making this possibilty more accessible to RPAN users.

## Installation  
There's 2 ways to install Snookey2:  
Method 1 (Recommended) - Install Python and do pip install snookey2 (follow the guide below!)  
Method 2 (Not really recommended unless you want the code for it) - Go to the Github page and download the .py file there!

## Using Snookey2  
This covers Method 1 of the Installation.  
Method 2 will not be covered here for simplicity.

Install Python for your system AND MAKE SURE if there's a checkbox that says "Add to Path" check that box. If you don't have that checkbox your most likely not on Windows so it's fine.

After it's done downloading open up your command prompt software (Command Prompt on Windows, Terminal on Mac, whatever on Linux) and do

```python -m pip install snookey2```

If that command doesn't work then try this command:

```python3 -m pip install snookey2```

If that doesn't work, it's mostly because of one of these problems:  
1. You didn't set Python to PATH (Windows)
2. Pip isn't set in PATH (Windows)
3. Pip didn't get downloaded (All Platforms)

Search up guides of your error or one of these problems to solve it, as I won't be going into how to fix them in this guide.

After doing the pip install command for Snookey2, go into command prompt and type this command:  

```snookey stream subreddit title```

But replace subreddit with the subreddit and title with the stream title.

IMPORTANT NOTE:  
If you want to do a stream with multiple words in the title you have to put quotation marks around the title.  
For example:

```snookey stream thegamerlounge "multiple word title"```

If your stream title is only one word, you don't need quotation marks.

```snookey stream thegamerlounge onewordtitle```

You can also view your stream chat (or someone else's stream chat) with this new command:

```snookey chat subreddit streamid```

The Stream ID can be found in the stream's URL and it's the 6 characters after the last /.

Make sure to do  
```snookey commands```  
if you want to know what all the commands are!

If done correctly, this will open a link in your browser allowing you to get an access code from Reddit     
**NOTE:** The Reddit app you are allowing access is not mine.  It is the client_id for the mobile, in this case android, Reddit app.    
One way you can confirm that I am not BS'ing you is by looking at [your apps](https://www.reddit.com/prefs/apps/) after allowing access.  
A third party application would normally appear here in the 'authorized applications' section with the developer's username.  This Reddit-built  
application does not follow the same rules.   

Just follow what the script says by reading the text, and join the Discord server!  
https://discord.gg/RZEYdn7

Disclaimer: I am not liable for your stupidity.  Please be responsible and follow the [Rules](https://www.redditinc.com/policies/broadcasting-content-policy).  Cheers.  

## Using Snookey2 in a Python Script  
So if you really want to, you can use Snookey2 in a Python script for whatever you're making!

First you have to do import snookey2 and you're set to do any of these commands!  
(The prefix for all of these commands is snookey2 so for example snookey2.commandhere)  

List of currently available functions:  
drp() - Enables Discord Rich Presence, so dont include it if you dont want it.  
info() - Info about Snookey2  
sublist() - Gives a list of all the supported subreddits  
tutorial() - Opens up the video tutorial  
discord() - Opens up the invite link to the Discord  
chat(subreddit, streamid) - Get the live stream chat on a stream (doesn't have to be yours)  
init(subreddit, title) - Actually run Snookey2  

and with that, Snookey2 is now a Python module to celebrate v3.0!

(Make sure to join the Discord for any questions!)
