import os
from google.genai import types

def write_file(working_directory, file_path, content):
    path = os.path.join(working_directory, file_path)
    if not os.path.abspath(path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        dir_path = os.path.dirname(path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except OSError as e:
        return f'Error: {e}'

schema_write_file= types.FunctionDeclaration(
    name="write_file",
    description=f"Write the specified content into the specified file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File which should be written to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content which should be written into the file",
            ),
        },
    ),
)
