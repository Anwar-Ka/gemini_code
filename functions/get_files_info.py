import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    if directory is None:
        directory = working_directory
    else:
        abs_working = os.path.abspath(working_directory)
        abs_target = os.path.abspath(os.path.join(working_directory, directory))
        
        if not abs_target.startswith(abs_working):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if  not os.path.isdir(abs_target):
        return f'Error: "{directory}" is not a directory'

    try:
        entries = os.listdir(abs_target)
        results = []
        for entry in entries:
            entry_path = os.path.join(abs_target, entry)
            try:
                size = os.path.getsize(entry_path)
                is_dir = os.path.isdir(entry_path)
                results.append(f"- {entry}: file_size={size} bytes, is_dir={is_dir}")
            except Exception as e:
                results.append(f"Error: Failed to access {entry}: {e}")
        return "\n".join(results)
    except Exception as e:
        return f"Error: {e}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)