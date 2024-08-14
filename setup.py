from setuptools import setup, find_packages

setup(
    name='bugBuddy',  
    version='0.1.0',  
    description='A CLI tool for interacting with OpenAI APIs and formatting responses.',
    author='Robert Avant',
    author_email='robertavant2003@gmail.com',
    url='https://github.com/robertavant1/openai-cli-tool.git',  
    packages=find_packages(),
    install_requires=[
        'click',
        'openai',
        'pygments',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': [
            'bugbuddy=openai_cli_tool.bugBuddy:get_response',  
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6', 
)