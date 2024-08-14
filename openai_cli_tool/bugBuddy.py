import os
import click
from openai import OpenAI
from pygments import highlight
import yaml
from pathlib import Path
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter

CONVERSATION_FILE = os.path.join('.', 'conversation.txt')
CONFIG_FILE = os.path.join('.', 'config.yaml')

# default configuration, can edit these settings in .yaml file
DEFAULT_SETTINGS = {
    "api-key": "<INSERT YOUR  OPENAI API KEY HERE>",
    "model": "gpt-3.5-turbo",
    # text color settings
    'text-color': '\033[1;96m', # Bright Cyan text
    'background-color': '\033[48;5;235m', # Gray Background
    'RESET': '\033[0m'  # Reset to default colors
}

pricing = {'gpt-4o': {'input': 0.0050, 'output': 0.0150}, # cost is per 1K tokens
           'gpt-4o-mini': {'input': 0.000150, 'output': 0.00060}}

def load_conversation(file_path):
    """ Loads currently saved conversations within the conversation.txt file.
        If file does not exist, it appends nothing to user prompt
    """
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read()
    return ""

def save_conversation(file_path, conversation):
    """ Saves current conversation to conversation.txt file
    """
    with open(file_path, 'a') as file:
        file.write(conversation)

def delete_conversation(file_path):
    """ If ---cleanup is enabled (default), conversation history is deleted before prompt is given
        Set --cleanup to false if you want to disable this feature so the AI remembers previous conversation
    """
    if os.path.exists(file_path):
        os.remove(file_path)

def get_token_usage(i_tokens, o_tokens, model):
    """ Prints out cost of each prompt based upon model used
    """
    input_cost = i_tokens * pricing[f'{model}']['input'] / 1000
    output_cost = o_tokens * pricing[f'{model}']['output'] / 1000
    total_cost = input_cost + output_cost
    return total_cost

def load_default_settings(default_config: str) -> dict:
    if not Path(default_config).exists():
        os.makedirs(os.path.dirname(default_config), exist_ok=True)
        with open(default_config, "w", encoding="utf-8") as file:
            yaml.dump(DEFAULT_SETTINGS, file, default_flow_style=False)

    with open(default_config, encoding="utf-8") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    # Update config file with any missing values to ensure proper functionality
    for key, value in DEFAULT_SETTINGS.items():
        if key not in config:
            config[key] = value
    return config

def print_text_block(text):
    """ Prints text block
        Change text and background colors in .yaml file
    """
    config = load_default_settings(CONFIG_FILE)
    TEXT_COLOR = config['text-color'].encode().decode('unicode_escape')
    BACKGROUND_COLOR = config['background-color'].encode().decode('unicode_escape')
    RESET = config['reset'].encode().decode('unicode_escape')
    return f"{BACKGROUND_COLOR}{TEXT_COLOR}{text}{RESET}"
    
def print_code_block(code):
    """ Prints code block (default lexer = Python)
        Change language lexer in .yaml file
    """
    config = load_default_settings(CONFIG_FILE)
    lexer_name = config['lexer']
    lexer = get_lexer_by_name(lexer_name.lower())
    highlighted_code = highlight(code, lexer, TerminalFormatter())
    return highlighted_code

@click.command()
@click.argument('prompt', nargs=-1, required = True)
@click.option('--file', type=click.File(mode="r"), required = False)
@click.option('--format', type = click.Choice(['text', 'code']) ,required=False, default = 'text')
def get_response(prompt, file, format):
    config = load_default_settings(CONFIG_FILE)
    try:
        client = OpenAI(api_key=config['api-key'])
    except:
        click.echo('API Key not found. Ensure that your key is set equal to the api_key variable in the .yaml file')
        return
    else:

        user_input = ""
        if prompt:
            user_input = f"\n\nUser input: {' '.join(prompt)}"

        if file:
            file_content = file.read()
            user_input += f"\n\n The following is the content of a file you should analyze:\n\n{file_content}"
 
        conversation_text = load_conversation(CONVERSATION_FILE)
        if conversation_text:
            user_input += conversation_text

        if config['enable-memory'] == 'false':
            delete_conversation(CONVERSATION_FILE)

        response = client.chat.completions.create(
            model=config['model'],
            messages= [
                {
                    "role": "system",
                    "content": 'Your job is to review code and answer any questions a user might have about it. This could include debugging, additional code generation to fit a use case, or explaining code to the user. You should also be able to suggest improvements to current code if possible, even if the current code functions properly.'
                },
                {
                    "role": "user",
                    "content": user_input 
                }
            ]
        )
    message = response.choices[0].message.content

    save_conversation(CONVERSATION_FILE, message)
    if format == 'text':
        click.echo(print_text_block(message))

    elif format == 'code':
        click.echo(print_code_block(message))

    usage = response.usage
    input_tokens = usage.prompt_tokens
    output_tokens = usage.completion_tokens
    cost = get_token_usage(input_tokens, output_tokens, config['model'])
    click.echo('Total cost for this prompt: $'+ str(cost))

if __name__ == '__main__':
    get_response()
