Secrets/credentials.json -> google authentication file
Secrets/secrets.env -> .env file that contains all keys for required APIs (currently Outlook and Google Calendar)
Secrets/Files.env -> .env file that contains Paths to any required files for updates (such as obsidian .md task file in a vault)

Secrets/Hidden Files/Completed.csv -> List of Completed tasks with their IDs
Secrets/Hidden Files/Pending.csv -> List of Pending tasks with their IDs
Secrets/Hidden Files/secretFunctions.py -> creates a dictonary or list (I haven't decided exactly how this will work) of functions that will update the tasklist DF and markdown file with tasks from external sources but may contain sensitive information (i.e. organizations and stuff) even if passwords and usernames are stored in the ENV files 