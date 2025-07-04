import os

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):    
    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_target.startswith(abs_working):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_target):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(abs_target, "r") as f:
            content = f.read(MAX_CHARS)
            remaining_char = f.read(1)
            if remaining_char:
                content += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content
    except Exception as e:
        return f"Error: {str(e)}"