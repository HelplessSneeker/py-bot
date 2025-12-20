import os
import argparse
from dotenv import load_dotenv
import config

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file 
from functions.call_function import call_function

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai
from google.genai import types

# Now we can access `args.user_prompt`
client = genai.Client(api_key=api_key)

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, 
        schema_write_file, 
        schema_get_file_content, 
        schema_run_python_file
        ],
)

config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=config.system_prompt
)


max_itterations = 20

while True:
    try:
        response = client.models.generate_content(
                model='gemini-2.5-flash-lite', 
                contents=messages,
                config=config
                )

        for candidate in response.candidates:
            messages.append(candidate.content)

        if response.usage_metadata == None:
            raise RuntimeError("Apie failed")

        if args.verbose:
            print(f"User prompt:{response.text}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        if response.function_calls != None:
            results = []
            for function in response.function_calls:
                result = call_function(function, args.verbose)
                if not result.parts[0].function_response.response:
                    raise Exception("Function Failed")
                results.append(result.parts[0])
                if args.verbose:
                    print(f"-> {result.parts[0].function_response.response}")
        else:
            print(response.text)


        messages.append(
            types.Content(
                role="user",
                parts=results,
            )
        )

        if len(response.candidates)  <= 0 and response.text != None:
            break
 
    except Exception as e:
        print(f"ERROR: {e}")

    if max_itterations < 0:
        break

    max_itterations -= 1
    print("test")




