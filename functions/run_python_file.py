import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_file_path = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if valid_file_path is False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_file) is False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if target_file.endswith(".py") is False:
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_file]
        if args is not None:
            command.extend(args)
        result = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)
        output = ""
        if result.returncode != 0:
             output +=f"Process exited with code {result.returncode}\n"
        if result.stdout == "" and result.stderr == "":
            output += "No output produced\n"
        else:
            if result.stdout != "":
                output += f"STDOUT:\n{result.stdout}\n"
            if result.stderr != "":
                output += f"STDERR:\n{result.stderr}\n"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"