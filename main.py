import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def llm_call():
    messages = []
    def prompt_runner():
        system_prompt = system_prompt = """
                        You are a helpful AI coding agent.

                        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

                        - List files and directories
                        - Read file contents
                        - Overwrite existing files or create and write new files if they don't exist
                        - Execute python files with optional arguments

                        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
                    """
        verbose = sys.argv[-1] == "--verbose"
        user_prompt = " ".join(sys.argv[1:-1]) if verbose else " ".join(sys.argv[1:])
        available_functions = types.Tool(function_declarations=[schema_get_files_info,
        schema_get_file_content, schema_write_file, schema_run_python_file])
        nonlocal messages
        messages.append(types.Content(role="user", parts=[types.Part(text=user_prompt)]))
        response = client.models.generate_content(model='gemini-2.0-flash-001',contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt,
        tools=[available_functions],))
        messages.append(types.Content(role="model", parts=[types.Part(text=response.text)]))

        if verbose:
            print(f"User prompt: {user_prompt}")
            if response.function_calls:
                for function_call in response.function_calls:
                    print(f'Calling function: {function_call.name} ({function_call.args})')
            else:
                print(response.text)
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
        else:
            if response.function_calls:
                for function_call in response.function_calls:
                    print(f'Calling function: {function_call.name} ({function_call.args})')
            else:
                print(response.text)

        return response.text

    return prompt_runner

def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <prompt_required> [--verbose]")
        sys.exit(1)

    conversation = llm_call()
    conversation()

if __name__ == "__main__":
    main()
