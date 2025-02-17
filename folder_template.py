import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] --- %(levelname)s: %(message)s')

list_files = [
    'src/__init__.py',
    'src/helper.py',
    'src/prompt.py',
    './.env',
    './setup.py',
    './app.py',
    'research/trials.ipynb'
]

for file in list_files:
    # Path is used to understand the file path based on the OS
    filepath = Path(file)
    
    filedir, filename = os.path.split(filepath)
    
    # Checking if there is a folder/directory or not in the path
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Directory '{filedir}' created for the filename '{filename}'")
    
    # Create the file if it does not exist or if it is empty
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, 'w') as f:
            pass
        logging.info(f"Creating an empty file '{filename}' in '{filedir}'")
    else:
        logging.info(f"File '{filename}' already exists in '{filedir}'")