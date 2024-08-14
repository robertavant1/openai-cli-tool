# bugBuddy ChatGPT CLI Tool

## Overview
Script for interacting with advanced ChatGPT models at a fraction of the cost (for the average user)through OpenAI's API. Designed to assist with debugging, additional code generation, and explanation of code

## Get your API Key
In order for this tool to function, you must get an API key from [platform.openai.com](https://platform.openai.com). You can login, go to your account and select *View API Keys*. Then select *Create new secret key*. You can then copy and paste this key into the config.yaml file (elaborated upon below).

# Usage
You can use the tool by typing 'bugBuddy.py in your terminal, followed by your prompt. Read below for more explanation of commands

## Order of commands
Due to the way that the click library parses arguments, the order in which you enter your commands will affect how the AI recieves your prompt. In general it is reccomended to structure your commands in the following way:

'bugBuddy.py *your prompt here* --file *File Path* --format *text or code*.

Note that --file and --format are optional arguments, and are not neccessary for the tool to run. 

## --file
If you want to have the tool read a file, you can type your prompt, followed by --file *INSERT FILE PATH HERE*. 

## --format
The default format that the tool displays is text. This is plain text, colored and displayed on a colored background. However, you can also print out a code block by adding --format code to the end of your prompt. This will tokenize the response and display it as it would be written in an IDE

# config.yaml File
This file allows you to adjust the default settings for the tool, including text and background colors, models, as well as the lexer to properly display code blocks for different languages. It also contains a place to input your API key, which is required for the tool to function. 

## Text and Background Colors
These colors are based upon ANSI color codes. In order to change them, you can visit this link (https://gist.github.com/JBlond/2fea43a3049b38287e5e9cefc87b2124) and paste the codes into their desired positions.

## Lexer
If you want to display code formatted in a language other than Python, you can change the 'lexer' variable to the name of the language in which you wish the code to be displayed in (i.e lexer : 'java' would out code formatted in Java). To see a full list of available lexers, visit (https://pygments.org/docs/lexers/).

## enable-memory
This variable is defaulted to 'false; in order to limit token usage and cost. However, if you would like for the tool to remember your conversation, you can change this variable to 'true'. This will append your previous conversation to your next prompt so that the model will remember it's past responses. To turn it off, return the variable to 'false', and the conversation history (conversation.txt) will be deleted.


=======
# openai-cli-tool
>>>>>>> ed472f8f7b3c85c8e4305b52f1e9ddf78ba485cb
