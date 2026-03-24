import os
from pathlib import Path
from dotenv import load_dotenv
import funcs
import constants as cnst


if __name__ == "__main__":
    funcs.resetDir()
    os.chdir("Keys")
    os.chdir("Secrets")
    load_dotenv("Files.env")
    load_dotenv("secrets.env")
    funcs.resetDir()


    taskFilePath = os.getenv("OBSIDIAN_TASK_FILE")
    print("---")
    with open(taskFilePath, 'r') as f:
        print(f.read())
    print("---")
    print(cnst.header)