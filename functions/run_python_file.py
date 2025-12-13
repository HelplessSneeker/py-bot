import os
import subprocess

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


