import os
import subprocess

def run_python_file(working_directory, file_path):
    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(working_directory,file_path))

    if not abs_target.startswith(abs_working):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_target):
        return f'Error: File "{file_path}" not found.'
    
    if not abs_target.lower().endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
            ["python3", file_path],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=working_directory
        )

        output_lines = []
        if result.stdout:
            output_lines.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output_lines.append(f"STDERR:\n{result.stderr}")
        if result.returncode != 0:
            output_lines.append(f"Process exited with code {result.returncode}")
        if not output_lines:
            return "No output produced."
        return "\n".join(output_lines)

    except Exception as e:
        return f"Error: executing Python file: {e}"
