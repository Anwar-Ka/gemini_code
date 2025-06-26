import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def llm_call(verbose=False):
    messages = []
    def prompt_runner(user_prompt):
        nonlocal messages
        messages.append(types.Content(role="user", parts=[types.Part(text=user_prompt)]))
        response = client.models.generate_content(model='gemini-2.0-flash-001',contents=messages)
        messages.append(types.Content(role="model", parts=[types.Part(text=response.text)]))

        if verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Gemini: {response.text}")
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
        else:
            print(response.text)

        return response.text

    return prompt_runner

def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <prompt_required> [--verbose]")
        sys.exit(1)

    verbose = sys.argv[-1] == "--verbose"
    user_prompt = " ".join(sys.argv[1:-1]) if verbose else " ".join(sys.argv[1:])

    conversation = llm_call(verbose=verbose)
    conversation(user_prompt)

if __name__ == "__main__":
    main()
