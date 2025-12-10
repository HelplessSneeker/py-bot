import os
import config

def get_file_content(working_directory, file_path):
    try:
        path = os.path.join(working_directory, file_path)
        if not os.path.abspath(path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(path, "r") as f:
            file_content_string = f.read(config.character_limit)
            return_string = file_content_string if len(file_content_string) < config.character_limit else f'{file_content_string} [...File "{file_path}" truncated at 10000 characters]'
            return return_string
    except OSError as e:
        return f"Error: {e}"

