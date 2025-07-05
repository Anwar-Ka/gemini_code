import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python import schema_run_python_file, run_python_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

messages = []

def llm_call():
    def prompt_runner():
        system_prompt = """
            You are claude_code a helpful AI coding agent.

            When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

            - List files and directories
            - Read file contents
            - Overwrite existing files or create and write new files if they don't exist
            - Execute python files with optional arguments

            All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """
        verbose = sys.argv[-1] == "--verbose"
        user_prompt = " ".join(sys.argv[1:-1]) if verbose else " ".join(sys.argv[1:])
        
        if not messages:
            messages.append(types.Content(role="user", parts=[types.Part(text=user_prompt)]))

        available_functions = types.Tool(function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file
        ])

        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions]
            )
        )

        for candidate in response.candidates:
            messages.append(candidate.content)

        return response, response.function_calls
    return prompt_runner

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    args = function_call_part.args

    if verbose:
        print(f'Calling function: {function_name} ({args})')
    else:
        print(f' - Calling function: {function_name}')

    agent_functions = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file
    }

    if function_name not in agent_functions:
        return types.Content(
            role="tool",
            parts=[types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"}
            )]
        )

    args["working_directory"] = "./calculator"

    try:
        function_result = agent_functions[function_name](**args)
    except Exception as e:
        function_result = f"Error while calling function: {str(e)}"

    return types.Content(
        role="tool",
        parts=[types.Part.from_function_response(
            name=function_name,
            response={"result": function_result}
        )]
    )

def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <prompt_required> [--verbose]")
        sys.exit(1)

    conversation = llm_call()
    iterations = 0
    max_iterations = 20
    verbose = sys.argv[-1] == "--verbose"

    while iterations < max_iterations:
        response, functions_called = conversation()

        if functions_called:
            for function_call in functions_called:
                function_result = call_function(function_call, verbose=verbose)

                messages.append(function_result)

                try:
                    result_payload = function_result.parts[0].function_response.response
                    if verbose:
                        print(f"-> {result_payload}")
                except Exception:
                    print("Fatal: Function call did not produce a valid response.")
                    sys.exit(1)
        else:
            print(response.text)
            break

        iterations += 1

if __name__ == "__main__":
    main()
