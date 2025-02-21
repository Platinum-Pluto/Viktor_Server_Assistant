
def print_manual(line):
    manual_texts = {
        "general": """
        Platinum Pluto Terminal

        NAME
            mytool - A custom command-line tool

        SYNOPSIS
            mytool [OPTION]...

        DESCRIPTION
            A detailed description of what your tool does.

        OPTIONS
            -h, --help
                Display this manual and exit.

            -a, --add
                Add a new entry to the JSON file.

            -e, --edit ID
                Edit an entry in the JSON file by ID.

            -d, --delete ID
                Delete an entry in the JSON file by ID.

            -m, --metadata PATH
                Retrieve metadata for the specified file or folder.
        """,
        "add": """
        ADD COMMAND

        SYNOPSIS
            mytool -a, --add

        DESCRIPTION
            Adds a new entry to the JSON file. The ID will be automatically assigned.
        """,
        "edit": """
        EDIT COMMAND

        SYNOPSIS
            mytool -e ID, --edit ID

        DESCRIPTION
            Edits an existing entry in the JSON file by ID. You will be prompted to enter new values for the fields.
        """,
        "delete": """
        DELETE COMMAND

        SYNOPSIS
            mytool -d ID, --delete ID

        DESCRIPTION
            Deletes an existing entry in the JSON file by ID.
        """,
        "metadata": """
        METADATA COMMAND

        SYNOPSIS
            mytool -m PATH, --metadata PATH

        DESCRIPTION
            Retrieves metadata for the specified file or folder, including creation time, modification time, and size.
        """
    }
    
    if line in manual_texts:
        print(manual_texts[line])
    else:
        print(manual_texts["general"])