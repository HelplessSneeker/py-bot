import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    path = os.path.join(working_directory, file_path)

    if not os.path.abspath(path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(path):
        return  f'Error: File "{file_path}" not found.'
    if file_path[-3:] != ".py":
        return f'Error: "{file_path}" is not a Python file.'

    return_string = ""

    args = ["python", path] + args

    try:
        output = subprocess.run(args, timeout=30, capture_output=True)
        if output:
            return_string = f"STDOUT: {output.stdout}\nSTDERR: {output.stderr}"
            if output.returncode != 0:
                return_string += f"\nProcess exited with code {output.returncode}"
        else:
            return_string += "No output produced"
        return return_string + "\n"
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file= types.FunctionDeclaration(
    name="run_python_file",
    description=f"Execute specified python file with provided args",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File which should be executed, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="List of Arguments wich should be passed to the python programm. If no Arguments are needed this can be left empty",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Single argument string"
                ),
            ),
        },
    ),
)
